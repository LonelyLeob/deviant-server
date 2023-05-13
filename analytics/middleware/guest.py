from django.http import HttpRequest
from ..models import Guest
from .simple import SimpleMiddleware


class GuestMiddleware(SimpleMiddleware):
    def __call__(self, request: HttpRequest):
        ip = self._process_ip(request)
        if ip:
            Guest.objects.get_or_create(ip=ip)
        return self._get_response(request)