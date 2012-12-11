from django.conf.urls.defaults import patterns, url

from .views import TutorDetailView, ListBySubjectView, ListByLevelView

urlpatterns = patterns('tutors.views',
    url(r'^(?P<pk>\d+)/$', TutorDetailView.as_view(), name='detail'),
    url(r'^subject/(?P<slug>[-\w]+)/$', ListBySubjectView.as_view(), name='list_by_subject'),
    url(r'^level/(?P<slug>[-\w]+)/$', ListByLevelView.as_view(), name='list_by_level'),
)
