from django.conf.urls.defaults import patterns, url

from .views import RegisterView, ValidateAccountView,\
    ForgotPasswordView, ForgotPasswordSuccessView, ResendActivationView,\
    DashboardView

urlpatterns = patterns('accounts.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^reset-activation/$', ResendActivationView.as_view(), name='resend_activation'),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^forgot-password-success/$', ForgotPasswordSuccessView.as_view(), name='forgot_password_success'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^validate/(?P<token>\w+)/$', ValidateAccountView.as_view(), name='validate'),

)
