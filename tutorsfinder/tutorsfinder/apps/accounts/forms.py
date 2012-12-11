from random import randint
import hashlib

from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory

from emails import send_using_template
from references.models import EmailTemplate, Subject, Level

from .models import PersonalInformation, TeachingExperience, \
       TeachingSubject, TeachingLevel, EducationBackground

class ForgotPasswordForm(forms.Form):
    
    email = forms.EmailField()

    def clean_email(self, *args, **kwargs):
        email = self.data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Email not found")
        else:
            return email

    def save(self, *args, **kwargs):
        user = User.objects.get(email=self.cleaned_data['email'])

        new_password = hashlib.sha1(str(randint(1,9999))).hexdigest()[0:6]

        user.set_password(new_password)
        user.save()

        context = {
            'new_password': new_password,

        }

        template = EmailTemplate.objects.get(slug='forgot-password')
        send_using_template(template, context, user.email)

        return user


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def get_user(self):
        email = self.data['email']
        if email and len(email) > 0:
            try:
                user = User.objects.get(email=email)
                return user
            except User.DoesNotExist:
                pass
        return None


    def clean_email(self, *args, **kwargs):
        email = self.data['email']
        user = self.get_user()
        if user is not None:
            if not user.validation_status.validated:
                message = "Account with this email is not activated yet, <a href='%s'>click here</a> to resend activation link." % reverse("accounts:resend_activation")
                raise forms.ValidationError(message)
            
            return email
        else:
            raise forms.ValidationError("Email does not exist")

    def clean_password(self, *args, **kwargs):
        email = self.data['email']
        password = self.data['password']

        if email and len(email) > 0:
            user = self.get_user()
            if user and not user.check_password(password):
                raise forms.ValidationError("Password is not valid")

        return password
    
    def save(self, *args, **kwargs):
        return self.get_user()


class RegisterForm(LoginForm):

    name = forms.CharField()

    def clean_email(self, *args, **kwargs):
        email = self.data['email']

        if self.get_user() is not None:
            raise forms.ValidationError("User with this email already exists")
        
        return email

    def clean_password(self, *args, **kwargs):
        password = self.data['password']
        if password and len(password) < 6 :
            raise forms.ValidationError("Password must be at least 6 characters")
        
        return password

    def save(self, *args, **kwrgs):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']
        user = User.objects.create_user(email[:29], email, password)
        user.save()
        user.details.set_name(name)
        return user


class ResendActivationForm(forms.Form):
    
    email = forms.EmailField()

    def clean_email(self, *args, **kwargs):
        email = self.data['email']
        try:
            user = User.objects.get(email=email)
            if user.validation_status.validated:
                raise forms.ValidationError("The account associated with this email is already activated.")
        except User.DoesNotExist:
            raise forms.ValidationError("Email not found")

        return email

    def save(self, *args, **kwargs):
        user = User.objects.get(email=self.cleaned_data['email'])
        user.validation_status.send_email()
        return user


class UpdatePasswordForm(forms.Form):

    current_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self, *args, **kwargs):
        current_password = self.data['current_password']
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Wrong password.")
        return current_password
            

    def clean_password(self, *args, **kwargs):
        password = self.data['password']

        if len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters')

        return password

    def clean_confirm_password(self, *args, **kwargs):
        password = self.data['password']
        confirm_password = self.data['confirm_password']

        if not password == confirm_password:
            raise forms.ValidationError("Passwords mismatched")

        return password

    def save(self, user):
        password = self.cleaned_data['password']

        user.set_password(password)
        user.save()

        return user


class PersonalInformationForm(forms.ModelForm):

    full_name = forms.CharField(max_length=255)
    street = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':'3'}))

    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].initial = self.instance.name
        self.fields['description'].label = 'About you'

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        
        details = super(PersonalInformationForm, self).save(*args, **kwargs)
        details.set_name(data['full_name'])

        return details

    class Meta:

        model = PersonalInformation
        exclude = ('user', 'longitude', 'latitude', 'enabled','post_code')


class TeachingExperienceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = None
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(TeachingExperienceForm, self).__init__(*args, **kwargs)
        self.fields['from_year'].label = 'From (year)' 
        self.fields['to_year'].label = 'To (year)'

    def save(self, *args, **kwargs):
        if self.user is not None:
            self.instance.user = self.user
        return super(TeachingExperienceForm, self).save(*args, **kwargs)

    class Meta:

        model = TeachingExperience
        exclude = ('user',)

TeachingExperienceInlineFormSet = inlineformset_factory(User, TeachingExperience, fk_name='user', form=TeachingExperienceForm, extra=1, max_num=5)


class TeachingSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=False)
    levels = forms.ModelMultipleChoiceField(queryset=Level.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TeachingSubjectsForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        data = self.cleaned_data

        user = self.user
        user.teaching_subjects.all().delete()
        user.teaching_levels.all().delete()

        for subject in data['subjects']:
            teaching_subject = TeachingSubject()
            teaching_subject.user = user
            teaching_subject.subject = subject
            teaching_subject.save()

        for level in data['levels']:
            teaching_level = TeachingLevel()
            teaching_level.user = user
            teaching_level.level = level
            teaching_level.save()

        return user



class EducationBackgroundForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = None
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(EducationBackgroundForm, self).__init__(*args, **kwargs)
        self.fields['qualification'].label = 'Degree' 
        self.fields['major'].label = 'Subject / Major'
        self.fields['institution'].label = 'University / College'

    def save(self, *args, **kwargs):
        if self.user is not None:
            self.instance.user = self.user
        return super(EducationBackgroundForm, self).save(*args, **kwargs)

    class Meta:

        model = EducationBackground
        exclude = ('user',)

EducationBackgroundInlineFormSet = inlineformset_factory(User, EducationBackground, fk_name='user', form=EducationBackgroundForm, extra=1, max_num=5)

