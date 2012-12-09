from django.contrib import admin
from django import forms

from fields.googlemapsearch import GoogleMapsWidget

from .models import ValidationStatus,\
   PersonalInformation, TeachingExperience, TeachingSubject,\
   TeachingLevel, EducationBackground


class PersonalInformationForm(forms.ModelForm):
    latitude = forms.CharField(label="Map",widget = GoogleMapsWidget(
        attrs={'map_canvas':'map_canvas','width': 450, 'height': 300,
            'longitude_id':'id_longitude',
            'city_id': 'id_city', 'country_id': 'id_country',
            'state_id': 'id_state', 'address_id':'id_address'}),

        error_messages={'required': 'Please select point from the map.'})
    longitude = forms.CharField(widget = forms.HiddenInput())

    class Meta:

        model = PersonalInformation


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

    form = PersonalInformationForm

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
