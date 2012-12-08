from random import randint
import hashlib

from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

from references.models import State, Area, Subject, Level, Qualification, EmailTemplate
from emails import send_using_template

def build_token(rand_min=1, rand_max=9999, range_max=5):
    # build token from a combination of randomized integer
    integers = [str(randint(rand_min, rand_max)) 
            for i in range(1, range_max)]
    token = hashlib.sha1(''.join(integers)).hexdigest()

    return token


class ResetPasswordRequest(models.Model):

    user = models.ForeignKey(User, related_name='reset_password_requests')
    token = models.CharField(max_length=1024)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def send_email(self):
        host = Site.objects.all()[0].domain
        reset_url = ''
        context = { 
                'reset_url' : "http://%s%s" % (host, reset_url), 
        }

        template = EmailTemplate.objects.get(slug='forgot-password')
        send_using_template(template, context, self.user.email)

    @staticmethod
    def create(user):
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
    def get_or_create(user):
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
        host = Site.objects.all()[0].domain
        validation_url = ''
        context = { 
                'validation_url' : "http://%s%s" % (host, validation_url), 
        }

        template = EmailTemplate.objects.get(slug='welcome-and-validation')
        send_using_template(template, context, self.user.email)

    class Meta:

        verbose_name_plural = "Validation statuses"


class PersonalInformation(models.Model):

    user = models.OneToOneField(User, related_name='details')
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(State)
    area = models.ForeignKey(Area)
    street = models.TextField(blank=True, null=True)
    post_code = models.CharField(max_length=16)
    hourly_rate = models.CharField(max_length=16)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField('Picture', blank=True, upload_to='picture/%Y/%m/%d')

    def set_name(self, name):
        first_name = name.split()[0]
        last_name = ' '.join(name.split()[1:])
        self.user.first_name = first_name
        self.user.last_name = last_name
        self.user.save()

    def __unicode__(self):
        return "%s" % self.user


class TeachingExperience(models.Model):

    user = models.ForeignKey(User, related_name='teaching_experiences')
    school = models.CharField(max_length=255)
    from_year = models.CharField(max_length=4)
    to_year = models.CharField(max_length=4)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.school)


class TeachingSubject(models.Model):

    user = models.ForeignKey(User, related_name='teaching_subjects')
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.subject.title)


class TeachingLevel(models.Model):

    user = models.ForeignKey(User, related_name='teaching_levels')
    level = models.ForeignKey(Level)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.level.title)


class EducationBackground(models.Model):

    user = models.ForeignKey(User, related_name='education_backgrounds')
    qualification = models.ForeignKey(Qualification)
    major = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_year = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.institution)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    ValidationStatus.get_or_create(instance)
