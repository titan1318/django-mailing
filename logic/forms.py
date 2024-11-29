from django import forms
from .models import Message, Client, Mailing, Attempt


class AddMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        labels = {
            'subject': 'Заголовок',
            'body': "Текст сообщения"
        }


class AddClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'surname', 'patronymic']
        labels = {'email': 'Эл. почта:',
                  'name': 'Имя:',
                  'surname': 'Фамилия:',
                  'patronymic': 'Отчество:'}


class AddMailing(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'period']
        labels = {'message': 'Сообщение',
                  'period': 'Периодичность'}


class AddAttempt(forms.ModelForm):
    class Meta:
        model = Attempt
        fields = ['mailing', 'client']
        labels = {'mailing': 'Название рассылки',
                  'client': 'Клиент'}
