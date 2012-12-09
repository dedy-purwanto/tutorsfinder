from django.conf.urls.defaults import patterns, url

from .views import LoginView, RegisterView, ValidateAccountView,\
    ForgotPasswordView, ForgotPasswordSuccessView

urlpatterns = patterns('accounts.views',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^forgot-password-success/$', ForgotPasswordSuccessView.as_view(), name='forgot_password_success'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^validate/(?P<token>\w+)/$', ValidateAccountView.as_view(), name='validate'),

)
