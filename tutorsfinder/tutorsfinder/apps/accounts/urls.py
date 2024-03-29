from django.conf.urls.defaults import patterns, url

from .views import RegisterView, ValidateAccountView,\
    ForgotPasswordView, ForgotPasswordSuccessView, ResendActivationView,\
    DashboardView, UpdatePasswordView, UpdatePersonalInformationView,\
    UpdateTeachingSubjectsView

urlpatterns = patterns('accounts.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^update-personal-information/$', UpdatePersonalInformationView.as_view(), name='update_personal_information'),
    url(r'^update-teaching-experience/$', 'update_teaching_experience', name='update_teaching_experience'),
    url(r'^delete-teaching-experience/(?P<pk>\d+)/$', 'delete_teaching_experience', name='delete_teaching_experience'),
    url(r'^update-teaching-subjects/$', UpdateTeachingSubjectsView.as_view(), name='update_teaching_subjects'),
    url(r'^update-education-background/$', 'update_education_background', name='update_education_background'),
    url(r'^delete-education-background/(?P<pk>\d+)/$', 'delete_education_background', name='delete_education_background'),
    url(r'^reset-activation/$', ResendActivationView.as_view(), name='resend_activation'),
    url(r'^update-password/$', UpdatePasswordView.as_view(), name='update_password'),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^forgot-password-success/$', ForgotPasswordSuccessView.as_view(), name='forgot_password_success'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^validate/(?P<token>\w+)/$', ValidateAccountView.as_view(), name='validate'),

)
