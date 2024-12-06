from django import forms
from django.forms import ModelForm

from mailing.models import Mailing, Client, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'  # Включить все поля из модели Рассылки


class MailingCreateForm(ModelForm):
    class Meta:
        model = Mailing
        exclude = ['owner', 'is_active']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['owner']


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ['owner']
