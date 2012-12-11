from django.conf.urls.defaults import patterns, url

from .views import TutorDetailView

urlpatterns = patterns('tutors.views',
    url(r'^(?P<pk>\d+)/$', TutorDetailView.as_view(), name='detail'),
)
