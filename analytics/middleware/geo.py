from django.http import HttpRequest
from django.contrib.gis.geoip2 import GeoIP2
from ..models import Human

class GeoPosMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self._get_response(request)
        ip = self._process_geo_pos(request)
        if ip:
            g = GeoIP2()
            human = Human.objects.create(city=g.city(ip), country=g.country_name(ip))
            human.save()
        return response

    def _process_geo_pos(self, request: HttpRequest)->(str|None):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip