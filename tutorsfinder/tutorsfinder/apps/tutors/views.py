from django.views.generic import DetailView
from django.http import Http404

from django.contrib.auth.models import User

from messages.forms import MessageForm


class TutorDetailView(DetailView):

    template_name = 'tutors/detail.html'

    def get_object(self, *args, **kwargs):
        user_pk = self.kwargs['pk']
        try:
            user = User.objects.get(pk=user_pk)
            return user
        except User.DoesNotExist:
            raise Http404()

    def get_context_data(self, *args, **kwargs):
        context = super(TutorDetailView, self).get_context_data(*args, **kwargs)

        user = self.get_object()

        prev_user = User.objects.filter(pk__lt=user.pk).order_by('-id')
        prev_user = prev_user[0] if prev_user.exists() else None

        next_user = User.objects.filter(pk__gt=user.pk).order_by('-id')
        next_user = next_user[0] if next_user.exists() else None

        context['prev_user'] = prev_user
        context['next_user'] = next_user

        context['message_form'] = MessageForm()

        return context


