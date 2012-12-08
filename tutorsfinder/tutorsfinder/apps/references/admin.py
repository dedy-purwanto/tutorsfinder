from django.contrib import admin

from .models import State, Area


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


admin.site.register(State, StateAdmin)
admin.site.register(Area, AreaAdmin)
