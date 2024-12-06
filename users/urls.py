from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from users import views
from users.apps import UsersConfig
from users.views import RegisterView, email_verification, ProfileView, reset_password, user_list, toggle_activation

app_name = UsersConfig.name

urlpatterns = [
    path('', cache_page(60)(views.home), name='home'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),       # вход
    path('logout/', LogoutView.as_view(), name='logout'),                               # выход
    path('register/', RegisterView.as_view(), name='register'),                         # регистрация
    path('users/email-confirm/<str:token>/', email_verification, name='email-confirm'),     # верификация почты
    path('reset_password/', reset_password, name='reset_password'),                   # сброс и восстановление пароля
    path('profile/', ProfileView.as_view(), name='profile'),                          # редактирование профиля
    path('users/', user_list, name='user_list'),
    path('users/toggle/<int:user_id>/', toggle_activation, name='toggle_activation'),

]