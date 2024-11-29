import pytz
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from logic.models import Mailing, Attempt
from django.core.mail import send_mail
from smtplib import SMTPException


def send_mailing():
    from logic.models import Mailing, Attempt
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(start_time__lte=current_datetime, status='launched')

    for mailing in mailings:
        for client in mailing.client_set.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False
                )
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status=True,
                    response='Success'
                )
            except SMTPException as e:
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status=False,
                    response=str(e)
                )


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, IntervalTrigger(minutes=1))
    scheduler.start()
