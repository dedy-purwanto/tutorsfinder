from django.views.generic import FormView
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.models import User

from .forms import MessageForm

class SendMessageView(FormView):
    
    form_class = MessageForm
    template_name = 'messages/send-message.html'

    def get(self, *args, **kwargs):
        raise Http404()

    def form_valid(self, form):
        user_pk = self.kwargs['user_pk']
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise Http404()

        form.save(user)

        message = "Your message has been sent to the tutor. He will receive it immediately."
        messages.add_message(self.request, messages.SUCCESS, _(message))

        return redirect(self.get_success_url(user))

    def get_success_url(self, user):
        return reverse("tutors:detail", args=[user.pk])

    def get_context_data(self, *args, **kwargs):
        context = super(SendMessageView, self).get_context_data(*args, **kwargs)

        user_pk = self.kwargs['user_pk']
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise Http404()

        context['recipient'] = user

        return context


