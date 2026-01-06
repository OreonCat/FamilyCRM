from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')
    extra_context = {'title': 'Регистрация'}

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
    form_class = AuthenticationForm
    extra_context = {'title': 'Регистрация'}

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('index'))

class UserProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['profile'].username
        return context

class UserUpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Редактировать профиль'}

    def get_object(self):
        return self.request.user

class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Сменить пароль'}

class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
