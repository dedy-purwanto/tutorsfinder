from random import randint
import hashlib

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

from references.models import EmailTemplate
from emails import send_using_template

def build_token(rand_min=1, rand_max=9999, range_max=5):
    # build token from a combination of randomized integer
    integers = [str(randint(rand_min, rand_max)) 
            for i in range(1, range_max)]
    token = hashlib.sha1(''.join(integers))

    return token


class ResetPasswordRequest(models.Model):

    user = models.ForeignKey(User, related_name='reset_password_requests')
    token = models.CharField(max_length=1024)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def send_email(self):
        pass

    @staticmethod
    def create_request(user):
        # build sha1 token from a combination of 3 randomized integer

        request = ResetPasswordRequest()
        request.user = user
        request.token = build_token()
        request.save()
        request.send_email()



class ValidationStatus(models.Model):

    user = models.OneToOneField(User, related_name='validation_status')
    token = models.CharField(max_length=1024)
    validated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_or_create(self, user):
        created = False
        try:
            status = ValidationStatus.objects.get(user=user)
        except ValidationStatus.DoesNotExist:
            status = ValidationStatus()
            status.user = user
            status.token = build_token()
            status.save()
            status.send_email()
            created = True

        return status, created

    def send_email(self):
        validation_url = ''
        context = {
            'validation_url' : validation_url,
        }
        send_using_template(EmailTemplate.objects.get(slug='welcome-and-validation'), context)

    class Meta:

        verbose_name_plural = "Validation statuses"


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    ValidationStatus.get_or_create(instance)
