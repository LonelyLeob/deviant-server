from django.http import HttpRequest
from django.contrib.gis.geoip2 import GeoIP2
from ..models import GeoCounter

class SimpleMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest):
        ip = self._process_ip(request)
        if ip and ip != "127.0.0.1":
            geocoder = GeoIP2()
            country = geocoder.country_name(ip)
            if GeoCounter.objects.filter(country=country).exists():
                counter = GeoCounter.objects.get(country=country)
                counter.requests_counter+=1
                counter.save()
            else:
                GeoCounter.objects.create(country=country).save()
        return self._get_response(request)

    def _process_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip