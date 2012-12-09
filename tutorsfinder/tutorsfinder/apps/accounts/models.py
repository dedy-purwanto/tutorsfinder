from random import randint
import hashlib

from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from references.models import State, Area, Subject, Level, Qualification, EmailTemplate
from emails import send_using_template

def build_token(rand_min=1, rand_max=9999, range_max=5):
    # build token from a combination of randomized integer
    integers = [str(randint(rand_min, rand_max)) 
            for i in range(1, range_max)]
    token = hashlib.sha1(''.join(integers)).hexdigest()

    return token


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
        validation_url = reverse("accounts:validate", args=[self.token])
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
    state = models.ForeignKey(State, blank=True, null=True)
    area = models.ForeignKey(Area, blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    post_code = models.CharField(max_length=16, blank=True, null=True)
    hourly_rate = models.CharField(max_length=16, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField('Picture', blank=True, null=True, upload_to='picture/%Y/%m/%d')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_or_create(user):
        created = False
        try:
            details = PersonalInformation.objects.get(user=user)
        except PersonalInformation.DoesNotExist:
            details = PersonalInformation()
            details.user = user
            details.save()

            created = True

        return details, created

    def set_name(self, name):
        first_name = name.split()[0]
        last_name = ' '.join(name.split()[1:])
        self.user.first_name = first_name
        self.user.last_name = last_name
        self.user.save()

    @property
    def name(self):
        if len(self.user.first_name) > 0 or len(self.user.last_name) > 0:
            name = "%s %s" % (self.user.first_name, self.user.last_name)
        else:
            name = self.user.email
        return "%s" % name

    @property
    def name_slug(self):
        return "%s" % slugify(self.name)

    def __unicode__(self):
        return "%s" % self.user


class TeachingExperience(models.Model):

    user = models.ForeignKey(User, related_name='teaching_experiences')
    school = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    from_year = models.CharField(max_length=4)
    to_year = models.CharField(max_length=4)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.school)


class TeachingSubject(models.Model):

    user = models.ForeignKey(User, related_name='teaching_subjects')
    subject = models.ForeignKey(Subject)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.subject.title)


class TeachingLevel(models.Model):

    user = models.ForeignKey(User, related_name='teaching_levels')
    level = models.ForeignKey(Level)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.level.title)


class EducationBackground(models.Model):

    user = models.ForeignKey(User, related_name='education_backgrounds')
    qualification = models.ForeignKey(Qualification)
    major = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_year = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.institution)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    ValidationStatus.get_or_create(instance)
    PersonalInformation.get_or_create(instance)
