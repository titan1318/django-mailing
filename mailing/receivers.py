from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from mailing.models import Mailing
from mailing.scheduler1 import remove_mailing_scheduler, reachedule_mailing, schedule_mailing


@receiver(post_save, sender=Mailing)
def schedule_job(instance: Mailing, created: bool, **kwargs):
    if created:
        print(f'Создан - {instance}')
        schedule_mailing(instance)

    else:
        print(f'Изменен - {instance}')
        reachedule_mailing(instance)



@receiver(post_delete, sender=Mailing)
def delete_job(instance: Mailing, **kwargs):
    print(f'Удален - {instance}')
    remove_mailing_scheduler(instance)
