from django.db import models

class State(models.Model):

    title = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.title


class Area(models.Model):

    state = models.ForeignKey(State, related_name='areas')
    title = models.CharField(max_length=255)

    def __unicode__(self):
        pass

    
