from django.views.generic import DetailView
from django.http import Http404

from django.contrib.auth.models import User

from messages.forms import MessageForm
from home.views import HomeView

from references.models import Subject, Level


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

        users = User.objects.filter(details__enabled=True, validation_status__validated=True)
        users = users.order_by('-pk')

        prev_user = users.filter(pk__lt=user.pk)
        prev_user = prev_user[0] if prev_user.exists() else None

        next_user = users.filter(pk__gt=user.pk).order_by('pk')
        next_user = next_user[0] if next_user.exists() else None

        context['prev_user'] = prev_user
        context['next_user'] = next_user

        context['message_form'] = MessageForm()

        return context


class ListBySubjectView(HomeView):

    template_name = 'tutors/list_by_subject.html'

    def get_subject(self):
        slug = self.kwargs['slug']
        try:
            subject = Subject.objects.get(slug=slug)
            return subject
        except Subject.DoesNotExist:
            raise Http404()

    def filter_tutors(self):
        tutors = super(ListBySubjectView, self).filter_tutors()
        subject = self.get_subject()
        tutors = tutors.filter(teaching_subjects__subject=subject)
        return tutors

    def get_context_data(self, *args, **kwargs):
        context = super(ListBySubjectView, self).get_context_data(*args, **kwargs)
        context['subject'] = self.get_subject()
        return context


class ListByLevelView(HomeView):

    template_name = 'tutors/list_by_level.html'

    def get_level(self):
        slug = self.kwargs['slug']
        try:
            level = Level.objects.get(slug=slug)
            return level
        except Level.DoesNotExist:
            raise Http404()

    def filter_tutors(self):
        tutors = super(ListByLevelView, self).filter_tutors()
        level = self.get_level()
        tutors = tutors.filter(teaching_levels__level=level)
        return tutors

    def get_context_data(self, *args, **kwargs):
        context = super(ListByLevelView, self).get_context_data(*args, **kwargs)
        context['level'] = self.get_level()
        return context

