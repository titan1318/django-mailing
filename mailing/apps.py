from time import sleep

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"
    verbose_name = "Рассылки"

    def ready(self):
        import mailing.receivers
        from mailing.scheduler1 import start_scheduler
        sleep(1)
        start_scheduler()
