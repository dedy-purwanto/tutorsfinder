from django.db import models
from django.template.defaultfilters import slugify

class State(models.Model):

    title = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.title


class Area(models.Model):

    state = models.ForeignKey(State, related_name='areas')
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.title


class Subject(models.Model):

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Subject, self).save(*args, **kwargs)

    class Meta:
        ordering = ['order', 'title']


class Level(models.Model):

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Level, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        ordering = ['order', 'title']


class Qualification(models.Model):

    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        ordering = ['order', 'title']


class EmailTemplate(models.Model):

    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    template = models.TextField()
    template_html = models.TextField(blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)

        return super(EmailTemplate, self).save()

    def __unicode__(self):
        return "%s" % self.name
    
