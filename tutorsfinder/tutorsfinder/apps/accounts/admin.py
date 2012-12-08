from django.contrib import admin

from .models import ResetPasswordRequest, ValidationStatus


class ResetPasswordRequestAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'token',
            'used',
            'date_created',
            'date_modified',
    )


class ValidationStatusAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'token',
            'validated',
            'date_created',
            'date_modified',
    )


admin.site.register(ResetPasswordRequest, ResetPasswordRequestAdmin)
admin.site.register(ValidationStatus, ValidationStatusAdmin)
