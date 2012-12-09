from django.views.generic import TemplateView

from django.contrib.auth.models import User

class HomeView(TemplateView):

    template_name = 'home/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)

        tutors = User.objects.filter(details__enabled=True, validation_status__validated=True)

        context['tutors'] = tutors

        return context
