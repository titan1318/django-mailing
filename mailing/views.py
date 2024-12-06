from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingCreateForm
from mailing.models import Mailing, Message, Client
from users.models import User


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='manager').exists():
                # Возвращаем все рассылки
                return Mailing.objects.all()
            # Возвращаем только рассылки, принадлежащих текущему пользователю
            return Mailing.objects.filter(owner=self.request.user)
        # Возвращаем пустой queryset для неаутентифицированных пользователей
        return Mailing.objects.none()


class MailingDetailView(DetailView):
    model = Mailing


def toggle_activation(request, mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)
    mailing.is_active = not mailing.is_active
    mailing.save()

    action = 'активирован' if mailing.is_active else 'деактивирован'
    messages.success(request, f'Пользователь {mailing.title} был {action}.')

    return redirect('mailing:mailing_detail', pk=mailing.id)  # Перенаправляем обратно в список пользователей


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingCreateForm

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Используем self.object.pk для получения первичного ключа обновленного объекта
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})
        # ------------------ адрес куда перенаправить после совершения действия

    # def form_valid(self, form):
    #     # отправка созданной рассылки по почте при создании
    #     obj = form.save()
    #     send_mailing_email(obj)
    #     return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingCreateForm

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            # Возвращаем только клиентов, принадлежащих текущему пользователю
            return Message.objects.filter(owner=self.request.user)
        # Возвращаем пустой queryset для неаутентифицированных пользователей
        return Message.objects.none()


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Используйте self.object.pk для получения первичного ключа обновленного объекта
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            # Возвращаем только клиентов, принадлежащих текущему пользователю
            return Client.objects.filter(owner=self.request.user)
        # Возвращаем пустой queryset для неаутентифицированных пользователей
        return Client.objects.none()


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Используйте self.object.pk для получения первичного ключа обновленного объекта
        return reverse_lazy('mailing:client_detail', kwargs={'pk': self.object.pk})


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


def mailing_status(request):
    mailings = Mailing.objects.prefetch_related('attempts').all()
    return render(request, 'mailing/mailing_status.html', {'mailings':mailings})
