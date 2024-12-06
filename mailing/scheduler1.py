import functools
import logging
from typing import Callable, Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.db import transaction
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from mailing.models import Mailing
from mailing.services1 import send_mailing_email

logger = logging.getLogger(__name__)


def update_mailing_status():
    """Обновляет статусы рассылок в зависимости от текущей даты"""
    now = timezone.now()
    mailings = Mailing.objects.all()
    for mailing in mailings:
        if now < mailing.at_start:
            mailing.status = Mailing.Status.CREATED
        elif now > mailing.at_end:
            mailing.status = Mailing.Status.FINISHED
        else:
            mailing.status = Mailing.Status.RUNNING
        mailing.save()


# def send_mailings():
#     """
#     Обновляет статусы рассылок в зависимости от текущей даты.
#     Получает и отправка всех активных рассылок, которые запущены в данный момент.
#     """
#     now = timezone.now()
#     mailings = Mailing.objects.all()
#     for mailing in mailings:
#         if now < mailing.at_start:
#             mailing.status = Mailing.Status.CREATED
#         elif now > mailing.at_end:
#             mailing.status = Mailing.Status.FINISHED
#         else:
#             mailing.status = Mailing.Status.RUNNING
#         mailing.save()
#
#     mailings = Mailing.objects.filter(is_active=True, status=Mailing.Status.RUNNING)
#     for mailing in mailings:
#         send_mailing_email(mailing.pk)


scheduler = BackgroundScheduler()

# Добавление хранилища заданий Django для хранения заданий в БД
scheduler.add_jobstore(DjangoJobStore(), 'default')


def wake_up_scheduler_after_transaction(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        transaction.on_commit(lambda: scheduler.wakeup())
        return result

    return wrapper


# Выполняется при получении отклика о создании рассылки
@wake_up_scheduler_after_transaction
def schedule_mailing(mailing: Mailing) -> None:
    if timezone.now() > mailing.at_start:
        send_mailing_email(mailing.pk)
        logger.info(f'Запустить рассылку "{mailing.title}" немедленно', mailing.id)
    job = scheduler.add_job(
        send_mailing_email,
        id=f'mailing_{mailing.pk}',
        trigger=_get_mailing_period_trigger(mailing),
        args=[mailing.pk],
        max_instances=1,
        replace_existing=True,
    )

    logger.debug(f'Рассылка "{mailing.title}" запланирована. Следующее время отправки {timezone.now()}.',
                 mailing.pk, job.next_run_time)


# Выполняется при получении отклика об изменении рассылки
@wake_up_scheduler_after_transaction
def reachedule_mailing(mailing: Mailing) -> None:
    job = scheduler.reschedule_job(job_id=f'mailing_{mailing.pk}', trigger=_get_mailing_period_trigger(mailing))
    logger.debug(f'Планировщик рассылка "{mailing.title}" обновлена. Следующее время отправки {timezone.now()}.',
                 mailing.pk, job.next_run_time)


# Выполняется при получении отклика об удалении рассылки
@wake_up_scheduler_after_transaction
def remove_mailing_scheduler(mailing: Mailing) -> None:
    if scheduler.get_job(job_id=f'mailing_{mailing.pk}'):
        scheduler.remove_job(job_id=f'mailing_{mailing.pk}')

        logger.debug(f'Планировщик рассылки удален')
    else:
        logger.warning(f'Планировщик рассылки %d не существует.', mailing.pk)


def _get_mailing_period_trigger(mailing: Mailing) -> CronTrigger:
    creat_trigger = functools.partial(CronTrigger, start_date=mailing.at_start)
    start_time_kwargs = {'hour': mailing.at_start.hour, 'minute': mailing.at_start.minute}

    match mailing.periodicity:
        case Mailing.Periodicity.CUSTOM:
            trigger = IntervalTrigger(seconds=10)

        case Mailing.Periodicity.DAILY:
            trigger = creat_trigger(day='*', **start_time_kwargs)

        case Mailing.Periodicity.WEEKLY:
            trigger = creat_trigger(day_of_week=mailing.at_start.weekday(), **start_time_kwargs)

        case Mailing.Periodicity.MONTHLY:
            trigger = creat_trigger(month='*', day=mailing.at_start, **start_time_kwargs)

        case _:
            raise ValueError(f'Неподдерживаемая периодичность: {mailing.periodicity}')

    return trigger


# Запуск планировщика
def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.start()
