from django.conf.urls.defaults import patterns, url

from .views import SendMessageView

urlpatterns = patterns('messages.views',
    url(r'^send-message/(?P<user_pk>\d+)/$', SendMessageView.as_view(), name='send_message'),

)
