from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.conf import settings
class GoogleMapsWidget(forms.HiddenInput):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=true',
             settings.STATIC_URL + 'js/googlemapshelper.js',
        )

    def render(self, name, value, attrs=None, choices=()):
        self.attrs['map_canvas'] = self.attrs.get('map_canvas', 'map_canvas')
        self.attrs['latitude'] = attrs['id']
        self.attrs['longitude'] =  self.attrs['longitude_id']
        self.attrs['base_point'] = self.attrs.get('base_point', u'0,0')
        self.attrs['width'] = self.attrs.get('width', 400)
        self.attrs['height'] = self.attrs.get('height', 400)
        self.attrs['country_city'] = self.attrs.get('country_city', u'')
        
        #self.attrs['city_id']
        #self.attrs['country_id']
        #self.attrs['state_id']
        #self.attrs['address_id']
        
        maps_html = render_to_string('fields/googlemapsearch.html', self.attrs)
        rendered = super(GoogleMapsWidget, self).render(name, value, attrs)
        return rendered + mark_safe(maps_html)