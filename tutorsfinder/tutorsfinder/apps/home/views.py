from django.views.generic import TemplateView

from django.contrib.auth.models import User

class HomeView(TemplateView):

    template_name = 'home/home.html'

    def filter_tutors(self):
        tutors = User.objects.filter(details__enabled=True, validation_status__validated=True)

        return tutors

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        tutors = self.filter_tutors()

        limit = 9

        page = self.request.GET.get('page', 1)
        page = int(page) - 1

        start_index = page * limit
        end_index = start_index + limit

        count = tutors.count()
        tutors = tutors.order_by('-pk')[start_index:end_index]


        if end_index < count:
            context['page_next'] = page + 2

        if start_index > 0:
            context['page_prev'] = page

        context['tutors'] = tutors

        return context
