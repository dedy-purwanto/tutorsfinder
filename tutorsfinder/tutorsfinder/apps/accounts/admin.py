from django.contrib import admin

from .models import ValidationStatus,\
   PersonalInformation, TeachingExperience, TeachingSubject,\
   TeachingLevel, EducationBackground


class ValidationStatusAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'token',
            'validated',
            'date_created',
            'date_modified',
    )

class PersonalInformationAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'date_created',
            'date_modified',
    )

class TeachingExperienceAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'school',
            'date_created',
            'date_modified',
    )

class TeachingSubjectAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'subject',
            'date_created',
            'date_modified',
    )

class TeachingLevelAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'level',
            'date_created',
            'date_modified',
    )

class EducationBackgroundAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user',
            'institution',
            'date_created',
            'date_modified',
    )


admin.site.register(ValidationStatus, ValidationStatusAdmin)
admin.site.register(PersonalInformation, PersonalInformationAdmin)
admin.site.register(TeachingExperience, TeachingExperienceAdmin)
admin.site.register(TeachingSubject, TeachingSubjectAdmin)
admin.site.register(TeachingLevel, TeachingLevelAdmin)
admin.site.register(EducationBackground, EducationBackgroundAdmin)
