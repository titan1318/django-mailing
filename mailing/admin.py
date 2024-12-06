from django.contrib import admin

from mailing.forms import MailingForm
from mailing.models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_first_name', 'email',  'pk',)

    def last_first_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    last_first_name.short_description = 'Имя клиента'  # Задаем имя столбца
    last_first_name.admin_order_field = 'last_name'  # Включаем сортировку по фамилии


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'pk',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'clients_count', 'status', 'pk',)
    list_filter = ('status',)

    form = MailingForm  # Используйте пользовательскую форму

    def clients_count(self, obj):
        return obj.clients.count()  # Возвращает количество клиентов для каждой рассылки

    clients_count.short_description = 'Количество клиентов'  # Пользовательское имя столбца


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('at_last_attempt', 'status', 'pk',)
    list_filter = ('status',)
