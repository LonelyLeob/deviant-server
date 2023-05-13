from django.http import HttpRequest
from django.contrib.gis.geoip2 import GeoIP2
from ..models import GeoCounter
from .simple import SimpleMiddleware

class GeoMiddleware(SimpleMiddleware):
    def __call__(self, request: HttpRequest):
        ip = self._process_ip(request)
        if ip and ip != "127.0.0.1":
            geocoder = GeoIP2()
            country = geocoder.country_name(ip)
            counter, _ = GeoCounter.objects.get_or_create(country=country)
            counter.requests_counter+=1
            counter.save()
        return self._get_response(request)