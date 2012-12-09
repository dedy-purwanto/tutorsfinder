from django.conf.urls import patterns, url

urlpatterns = patterns('references.views',
    url(r'fetch-areas/$', 'fetch_areas', name='fetch_areas'),
)
