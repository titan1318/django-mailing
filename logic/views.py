from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from logic.forms import AddMessage, AddClient, AddMailing, AddAttempt
from logic.models import Message, Client, Mailing, Attempt, BlogPost
from django.views.generic import ListView, DetailView, TemplateView
from django.core.cache import cache


class HomePageView(TemplateView):
    template_name = 'logic/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if cache.get('home_page_data'):
            context.update(cache.get('home_page_data'))
        else:
            home_page_data = {
                'total_mailings': Mailing.objects.count(),
                'active_mailings': Mailing.objects.filter(status='launched').count(),
                'unique_clients': Client.objects.count(),
                'random_articles': BlogPost.objects.order_by('?')[:3],
            }
            cache.set('home_page_data', home_page_data, timeout=60 * 5)
            context.update(home_page_data)

        return context


class BlogListView(ListView):
    model = BlogPost
    template_name = 'logic/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 5


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'logic/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


class MailingReportView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'logic/mailing_report.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.annotate(
            total_attempts=Count('attempt'),
            successful_attempts=Sum('attempt__status')
        )


class HomeTemplateView(TemplateView):
    template_name = 'logic/home.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'logic/add_message.html'
    form_class = AddMessage
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SuccessTemplateView(TemplateView):
    template_name = 'logic/success.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'logic/add_client.html'
    form_class = AddClient
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = 'logic/add_mailing.html'
    form_class = AddMailing
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AttemptCreateView(LoginRequiredMixin, CreateView):
    model = Attempt
    template_name = 'logic/attempt.html'
    form_class = AddAttempt
    success_url = reverse_lazy('success')


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'logic/mailing_detail.html'

    def test_func(self):
        return self.get_object().owner == self.request.user
