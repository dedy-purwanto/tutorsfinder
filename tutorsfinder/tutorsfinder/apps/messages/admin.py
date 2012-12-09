from django.contrib import admin


from .models import Message

class MessageAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'recipient',
            'sender_email',
            'date_created',
    )

admin.site.register(Message, MessageAdmin)
