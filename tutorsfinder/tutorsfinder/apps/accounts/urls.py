from django.conf.urls.defaults import patterns, url

from .views import RegisterView, ValidateAccountView,\
    ForgotPasswordView, ForgotPasswordSuccessView, ResendActivationView,\
    DashboardView, UpdatePasswordView, UpdatePersonalInformationView

urlpatterns = patterns('accounts.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^update-personal-information/$', UpdatePersonalInformationView.as_view(), name='update_personal_information'),
    url(r'^reset-activation/$', ResendActivationView.as_view(), name='resend_activation'),
    url(r'^update-password/$', UpdatePasswordView.as_view(), name='update_password'),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^forgot-password-success/$', ForgotPasswordSuccessView.as_view(), name='forgot_password_success'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^validate/(?P<token>\w+)/$', ValidateAccountView.as_view(), name='validate'),

)
