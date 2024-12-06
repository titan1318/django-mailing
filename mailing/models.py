from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': False}


class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name="Электронной почты", unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name="Тема сообщения")
    message = models.TextField(verbose_name="Сообщение")
    preview = models.ImageField(verbose_name="Превью", upload_to='message/preview', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания", **NULLABLE)
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title} от {self.created_at}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    class Periodicity(models.TextChoices):
        CUSTOM = 'C', 'Custom'
        DAILY = 'D', 'Ежедневно'
        WEEKLY = 'W', 'Еженедельно'
        MONTHLY = 'M', 'Ежемесячно'

    class Status(models.TextChoices):
        CREATED = 'C', 'Создана'
        RUNNING = 'R', 'Запущена'
        FINISHED = 'F', 'Завершена'

    title = models.CharField(max_length=100, verbose_name="Название рассылки")
    preview = models.ImageField(verbose_name="Превью", upload_to='mailing/preview', **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания", **NULLABLE)
    clients = models.ManyToManyField(Client, verbose_name="Список клиентов", blank=True)
    at_start = models.DateTimeField(verbose_name='Дата и время начала отправки')
    at_end = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    periodicity = models.CharField(max_length=1, choices=Periodicity.choices, verbose_name='Периодичность')
    status = models.CharField(max_length=1, verbose_name="Статус рассылки", choices=Status.choices,
                              default=Status.CREATED)
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True, verbose_name="")

    def __str__(self):
        return f'Рассылка {self.pk}: {self.title} от {self.created_at},  периодичность - {self.periodicity}, количество клиентов - {self.clients.count()} чел. (статус - {self.status})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Attempt(models.Model):
    class Status(models.IntegerChoices):
        SUCCESS = 1, 'Успешно'
        FAILURE = 2, 'Неудачно'

    at_last_attempt = models.DateTimeField(verbose_name='Дата последней попытки', auto_now_add=True)
    status = models.SmallIntegerField(choices=Status.choices, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE, default="")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name='попытки')

    def __str__(self):
        return f'Попытка отправки {self.mailing} от {self.at_last_attempt}'

    class Meta:
        ordering = ['-at_last_attempt']
