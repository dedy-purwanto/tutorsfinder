from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from .models import ValidationStatus, ResetPasswordRequest


class LoginView(FormView):

    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.data['password'])
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        return reverse("home:home")


class RegisterView(FormView):

    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.data['password'])
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        return reverse("home:home")


class ValidateAccountView(TemplateView):

    def get(self, *args, **kwargs):
        token = self.kwargs['token']
        try:
            status = ValidationStatus.objects.get(validated=False, token=token)
        except ValidationStatus.DoesNotExist:
            raise Http404()
        else:
            status.validated = True
            status.save()
            message = "Your account has been confirmed. Thank you."
            messages.add_message(self.request, messages.SUCCESS, _(message))
            return redirect(reverse("home:home"))


class ForgotPasswordView(FormView):

    form_class = ForgotPasswordForm
    template_name = 'accounts/forgot-password.html'

    def form_valid(self, form):
        form.save()

        message = "A reset password link has been sent to your email. Please click the link to reset your password."
        messages.add_message(self.request, messages.SUCCESS, _(message))

        return redirect(reverse("accounts:forgot_password"))


class ResetPasswordView(FormView):

    form_class = ResetPasswordForm
    template_name = 'accounts/reset-password.html'

    def get(self, *args, **kwargs):
        token = self.kwargs['token']
        try:
            ResetPasswordRequest.objects.get(used=False, token=token)
        except ResetPasswordRequest.DoesNotExist:
            raise Http404()
        
        return super(ResetPasswordView, self).get(*args, **kwargs)

    def form_valid(self, form):
        form.save(self.kwargs['token'])

        message = "You have changed your password. You can now login with your new password."
        messages.add_message(self.request, messages.SUCCESS, _(message))

        return redirect(reverse("accounts:login"))


