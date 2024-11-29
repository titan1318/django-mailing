from django.apps import AppConfig
from time import sleep


class LogicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logic'

    def ready(self):
        from .tasks import start_scheduler
        sleep(2)
        start_scheduler()
