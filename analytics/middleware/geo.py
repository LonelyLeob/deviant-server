from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
from ..models import GeoCounter
from girl.models import Girl
from .simple import SimpleMiddleware, IPMiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist, BadRequest


class GeoMiddleware(SimpleMiddleware, IPMiddlewareMixin):
    def __call__(self, request):
        if "admin" in request.get_full_path():
            return self._get_response(request)
        ip = self._process_ip(request)
        if ip and ip != "127.0.0.1":
            origin = request.headers.get('Origin')
            try:
                girl = Girl.objects.get(domain=origin)
            except:
                return HttpResponse(status=400)
            geocoder = GeoIP2()
            country = geocoder.country_name(ip)
            counter, _ = GeoCounter.objects.get_or_create(country=country, girl=girl)
            counter.requests_counter+=1
            counter.save()
        return self._get_response(request)