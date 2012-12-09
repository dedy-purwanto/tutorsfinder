from django.conf.urls.defaults import patterns, url

from .views import LoginView, RegisterView

urlpatterns = patterns('accounts.views',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),

)
