from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.subject


class Client(models.Model):
    email = models.EmailField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Mailing(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('completed', 'Завершена'),
        ('launched', 'Запущена'),
    ]

    start_time = models.DateTimeField(auto_now=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    period = models.CharField(max_length=64, choices=PERIOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Создан')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailings')

    def __str__(self):
        return f"Mailing {self.id} - {self.get_status_display()}"


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='attempts')
    attempt_time = models.DateTimeField(default=now)
    status = models.BooleanField(default=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Attempt {self.id} - {'Successful' if self.status else 'Unsuccessful'}"
