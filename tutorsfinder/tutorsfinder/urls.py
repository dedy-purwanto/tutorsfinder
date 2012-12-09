from django.conf.urls import patterns, include, url
from django.contrib import admin

from accounts.views import LoginView, LogoutView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('home.urls', namespace='home')),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    url(r'^admin/', include(admin.site.urls)),
)
