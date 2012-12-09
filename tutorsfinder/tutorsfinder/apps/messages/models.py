from django.db import models
from django.contrib.auth.models import User

from references.models import EmailTemplate
from emails import send_using_template

class Message(models.Model):

    recipient = models.ForeignKey(User, related_name='messages')
    sender_email = models.EmailField()
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def send_email(self):

        context = {
            'message' : self,
        }
        template = EmailTemplate.objects.get(slug='contact-tutor')
        send_using_template(template, context, self.recipient.email)
