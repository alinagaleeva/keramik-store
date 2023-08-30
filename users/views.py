from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from common.views import TitleMixin

from .forms import UserRegistrationForm, UsersLoginFrom
from .models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UsersLoginFrom
    title = 'account'


class UserRegistrationView(TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/create_account.html'
    success_url = reverse_lazy('login')
    title = 'create account'


class UserProfileView(TitleMixin, TemplateView):
    template_name = 'users/profile.html'
    title = 'account'


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Keramik - verification email'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
