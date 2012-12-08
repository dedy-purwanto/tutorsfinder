from django.db import models
from django.contrib.auth.models import User

class ResetPasswordRequest(models.Model):

    user = models.ForeignKey(User, related_name='reset_password_requests')
    token = models.CharField(max_length=1024)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class ValidationStatus(models.Model):

    user = models.OneToOneField(User, related_name='validation_status')
    token = models.CharField(max_length=1024)
    validated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Validation Statuses"
