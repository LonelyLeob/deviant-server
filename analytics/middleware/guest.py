from django.http import HttpRequest
from ..models import Guest
from girl.models import Girl
from .simple import SimpleMiddleware, IPMiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist, BadRequest


class GuestMiddleware(SimpleMiddleware, IPMiddlewareMixin):
    def __call__(self, request: HttpRequest):
        ip = self._process_ip(request)
        origin = request.headers.get('Origin')
        if origin:
            try:
                girl = Girl.objects.get(domain=origin)
            except Exception:
                raise BadRequest
        if ip:
            Guest.objects.get_or_create(ip=ip, girl=girl)
        return self._get_response(request)