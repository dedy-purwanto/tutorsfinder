from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from accounts.views import LoginView, LogoutView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('home.urls', namespace='home')),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    url(r'^references/', include('references.urls', namespace='references')),

    url(r'^tutor/', include('tutors.urls', namespace='tutors')),

    url(r'^messages/', include('messages.urls', namespace='messages')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
