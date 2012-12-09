from django.views.generic import DetailView
from django.http import Http404

from django.contrib.auth.models import User


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

        return context


