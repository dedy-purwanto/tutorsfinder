from django.conf.urls.defaults import patterns, url

from .views import LoginView, RegisterView, ValidateAccountView,\
    ForgotPasswordView, ResetPasswordView

urlpatterns = patterns('accounts.views',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^validate/(?P<token>\w+)/$', ValidateAccountView.as_view(), name='validate'),
    url(r'^reset-password/(?P<token>\w+)/$', ResetPasswordView.as_view(), name='reset_password'),

)
