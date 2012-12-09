from django import forms
from django.contrib.auth.models import User

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
        if self.get_user() is not None:
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
        password = self.cleaned_data['password']
        user = User.objects.create_user(email[:29], email, password)
        user.save()
        return user


