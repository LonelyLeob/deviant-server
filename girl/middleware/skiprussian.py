from django.http import HttpRequest
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponseRedirect
from ..models import Girl

class SkipperMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest):
        ip = self._process_ip(request)
        if ip:
            geocoder = GeoIP2()
            if geocoder.country_name() == "Russia":
                if len(request.path.split("/")) >= 2:
                    girl_slug = request.path.split("/")[2]
                    girl = Girl.objects.filter(slug=girl_slug).first()
                    tg_link_to_redirect = girl.links.filter(title = "Telegram").first().link
                    return HttpResponseRedirect(tg_link_to_redirect)
        return self._get_response(request)

    def _process_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip