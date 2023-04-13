from django.http import HttpRequest
from django.contrib.gis.geoip2 import GeoIP2
from ..models import Geo

class GeoPosMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self._get_response(request)
        ip = self._process_ip(request)
        if ip:
            if not Geo.objects.filter(ip=ip).exists():
                geocoder = GeoIP2()
                geopos = Geo.objects.create(city=geocoder.city(ip)["city"], country=geocoder.country_name(ip), ip=ip)
                geopos.save()
        return response

    def _process_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip