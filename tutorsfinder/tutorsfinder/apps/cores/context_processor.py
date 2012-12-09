from django.contrib.sites.models import Site
def base_context(request):
    site_name = Site.objects.all()[0].name

    return {
        'SITE_NAME' : site_name,
    }
