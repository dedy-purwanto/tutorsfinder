from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .forms import LoginForm, RegisterForm


class LoginView(FormView):

    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=form.user.username, password=form.data['password'])
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
        user = authenticate(username=form.user.username, password=form.data['password'])
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        return reverse("home:home")


