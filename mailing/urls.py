from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, ClientListView, \
    ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView, toggle_activation, mailing_status

app_name = MailingConfig.name

urlpatterns = [
                  path('', MailingListView.as_view(), name='mailing_list'),
                  path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
                  path('mailing/create', MailingCreateView.as_view(), name='mailing_create'),
                  path('mailing/<int:pk>/update', MailingUpdateView.as_view(), name='mailing_update'),
                  path('mailing/<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),
                  path('mailing/toggle/<int:mailing_id>/', toggle_activation, name='toggle_activation'),

                  path('message/list', MessageListView.as_view(), name='message_list'),
                  path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
                  path('message/create', MessageCreateView.as_view(), name='message_create'),
                  path('message/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
                  path('message/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),

                  path('client/list', ClientListView.as_view(), name='client_list'),
                  path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
                  path('client/create', ClientCreateView.as_view(), name='client_create'),
                  path('client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
                  path('client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),

                  path('mailing/status_list', mailing_status, name='mailing_status'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
