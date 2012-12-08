from django.contrib import admin

from .models import State, Area, Subject, Level, Qualification, EmailTemplate


class StateAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'title',
    )


class AreaAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'state',
            'title',
    )


class SubjectAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'title',
            'order',
    )


class LevelAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'title',
            'order',
    )


class QualificationAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'title',
            'order',
    )


class EmailTemplateAdmin(admin.ModelAdmin):
    fields = ('name', 'subject', 'template', 'template_html', )

    list_display = (
            'id',
            'name',
            'slug',
    )


admin.site.register(State, StateAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
