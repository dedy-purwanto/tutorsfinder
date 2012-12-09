from django import forms

from .models import Message

class MessageForm(forms.Form):

    email = forms.EmailField()
    content = forms.CharField()

    def save(self, user):
        data = self.cleaned_data
        message = Message()
        message.recipient = user
        message.sender_email = data['email']
        message.content = data['content']
        message.save()
        message.send_email()

        return message

