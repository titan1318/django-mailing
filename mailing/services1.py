import logging
import smtplib

from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mailing.models import Attempt, Mailing

logger = logging.getLogger(__name__)


def send_mailing_email(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)

    logger.info('Выполнение рассылки с id %s', mailing.id)

    recipient_list = [client.email for client in mailing.clients.all()]

    responses = []

    try:
        # Отправляем письмо
        server_response = send_mail(
            subject=mailing.message.title,
            message=mailing.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        # Записываем успешную попытку
        Attempt.objects.create(
            status=Attempt.Status.SUCCESS,
            server_response=f'Письмо по адресу {recipient_list} отправлено, ответ сервиса: {server_response}.',
            mailing=mailing
        )
        responses.append(f'Письмо на {recipient_list} отправлено.')

    except smtplib.SMTPException as e:
        # При ошибке почтовика получаем ответ сервиса - ошибка (е)
        Attempt.objects.create(
            status=Attempt.Status.FAILURE,
            server_response=str(e),
            mailing=mailing
        )
        responses.append(f'Не удалось отправить письмо по адресу {recipient_list}: {str(e)}.')

    return responses
