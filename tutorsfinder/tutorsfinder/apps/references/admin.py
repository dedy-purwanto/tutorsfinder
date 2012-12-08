from django.contrib import admin

from .models import State, Area, Subject, Level, Qualification


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


admin.site.register(State, StateAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Qualification, QualificationAdmin)
