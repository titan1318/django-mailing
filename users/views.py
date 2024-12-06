import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from mailing.models import Mailing, Client
from blog.models import Post

import secrets


@login_required
def home(request):

    mailings = Mailing.objects.filter(owner=request.user)
    # Получение общего количества рассылок
    total_mailings = mailings.count()

    # Получение количества рассылок со статусом RUNNING
    running_mailings = mailings.filter(status='R').count()

    # Получение количества клиентов, принадлежащих текущему пользователю
    user_clients = Client.objects.filter(owner=request.user).count()

    # Получение трех случайных постов из модели Post
    random_posts = Post.objects.order_by('?')[:3]

    context = {
        'total_mailings': total_mailings,
        'running_mailings': running_mailings,
        'user_clients': user_clients,
        'random_posts': random_posts,
    }

    return render(request, 'users/main.html', context)  # Отображение main.html для авторизованных пользователей

def login_view(request):
    return render(request, 'users/login.html')  # Отображение login.html для неавторизованных пользователей


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'

        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_random_password(length=8):
    """Генерирует случайный пароль."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.password = make_password(new_password)  # Хэшируйте новый пароль
            user.save()

            # Send email with the new password
            send_mail(
                subject='Ваш новый пароль',
                message=f'Ваш новый пароль: {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )

            messages.success(request, 'Новый пароль отправлен на ваш адрес электронной почты.')
            return redirect('users:login')  # Redirect to login page after successful reset

        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким адресом электронной почты не найден.')

    return render(request, 'users/reset_password.html')


def user_list(request):
    user = request.user
    if user.is_authenticated and user.groups.filter(name='manager').exists():
        users = User.objects.all()
        return render(request, 'users/user_list.html', {'users': users})
    raise PermissionDenied


def toggle_activation(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()

    action = 'активирован' if user.is_active else 'деактивирован'
    messages.success(request, f'Пользователь {user.email} был {action}.')

    return redirect('users:user_list')  # Перенаправляем обратно в список пользователей