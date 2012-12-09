import json

from django.http import HttpResponse

from .models import Area

def fetch_areas(request):
    state_pk = request.GET.get('state', None)
    areas_dict = {}
    if state_pk:
        areas = Area.objects.filter(state__pk=state_pk)
        if areas.exists():
            for area in areas:
                areas_dict[area.pk] = area.title

    return HttpResponse(json.dumps(areas_dict))
