from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

from cores.views import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, \
        ResendActivationForm, UpdatePasswordForm, PersonalInformationForm,\
        TeachingExperienceForm, TeachingExperienceInlineFormSet
from .models import ValidationStatus, PersonalInformation, TeachingExperience


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
        return reverse("accounts:dashboard")


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


class UpdatePasswordView(LoginRequiredMixin, FormView):

    form_class = UpdatePasswordForm
    template_name = 'accounts/update-password.html'

    def get_form(self, *args, **kwargs):
        return self.form_class(self.request.POST or None, user=self.request.user)

    def form_valid(self, form):
        form.save(self.request.user)
        message = "Password updated."
        messages.add_message(self.request, messages.SUCCESS, _(message))
        return redirect(reverse("accounts:update_password"))


class UpdatePersonalInformationView(LoginRequiredMixin, UpdateView):

    template_name = 'accounts/update-personal-information.html'
    model = PersonalInformation
    form_class = PersonalInformationForm

    def get_form(self, *args, **kwargs):
        return self.form_class(self.request.POST or None, self.request.FILES or None, instance=self.get_object())

    def get_object(self, *args, **kwargs):
        return self.request.user.details

    def get_success_url(self, *args, **kwargs):
        return reverse('accounts:update_personal_information')


@login_required
def update_teaching_experience(request):
    context = {}
    user = request.user
    if not user.teaching_experiences.exists():
        form = TeachingExperienceForm(request.POST or None, user=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse("accounts:update_teaching_experience"))

        context['form'] = form
    else:
        formset = TeachingExperienceInlineFormSet(request.POST or None, instance=user)
        if formset.is_valid():
            formset.save()
            return redirect(reverse("accounts:update_teaching_experience"))
        context['formset'] = formset

    return render_to_response("accounts/update-teaching-experience.html", context,
                            RequestContext(request))

@login_required
def delete_teaching_experience(request, pk):
    user = request.user
    try:
        experience = TeachingExperience.objects.get(pk=pk, user=user)
        experience.delete()
        message = "1 Teaching experience has been deleted."
        messages.add_message(request, messages.SUCCESS, _(message))
        return redirect(reverse("accounts:update_teaching_experience"))
    except TeachingExperience.DoesNotExist:
        raise Http404()
