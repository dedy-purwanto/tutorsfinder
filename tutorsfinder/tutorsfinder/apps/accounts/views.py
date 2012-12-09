from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from cores.views import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResendActivationForm
from .models import ValidationStatus


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


class LogoutView(TemplateView):

    def get(self, *args, **kwargs):
        request = self.request

        logout(request)

        return redirect(reverse("home:home"))


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
            message = "Your account has been activated. Thank you."
            messages.add_message(self.request, messages.SUCCESS, _(message))
            return redirect(reverse("home:home"))


class ForgotPasswordView(FormView):

    form_class = ForgotPasswordForm
    template_name = 'accounts/forgot-password.html'

    def form_valid(self, form):
        form.save()
        return redirect(reverse("accounts:forgot_password_success"))


class ForgotPasswordSuccessView(TemplateView):

    template_name = 'accounts/forgot-password-success.html'


class ResendActivationView(FormView):

    form_class = ResendActivationForm
    template_name = 'accounts/resend-activation.html'

    def form_valid(self, form):
        form.save()
        message = "Activation link sent."
        messages.add_message(self.request, messages.SUCCESS, _(message))
        return redirect(reverse("accounts:resend_activation"))


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)

        return context
