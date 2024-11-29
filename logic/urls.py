from django.urls import path
from .views import HomeTemplateView, MessageCreateView, SuccessTemplateView, ClientCreateView, MailingCreateView, \
    AttemptCreateView, MailingReportView, BlogListView, BlogDetailView, HomePageView

urlpatterns = [
    path('mailing_report/', MailingReportView.as_view(), name='mailing_report'),
    path('', HomeTemplateView.as_view(), name='homepage'),
    path('add_message/', MessageCreateView.as_view(), name='add_message'),
    path('add_client/', ClientCreateView.as_view(), name='add_client'),
    path('add_mailing', MailingCreateView.as_view(), name='add_mailing'),
    path('add_attempt', AttemptCreateView.as_view(), name='add_attempt'),
    path('success/', SuccessTemplateView.as_view(), name='success'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('', HomePageView.as_view(), name='home'),
]
