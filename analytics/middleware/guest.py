from django.http import HttpResponse
from ..models import Guest
from girl.models import Girl
from .simple import SimpleMiddleware, IPMiddlewareMixin


class GuestMiddleware(SimpleMiddleware, IPMiddlewareMixin):
    def __call__(self, request):
        if "admin" in request.get_full_path() or "media" in request.get_full_path():
            return self._get_response(request)
        ip = self._process_ip(request)
        origin = request.headers.get('Origin')
        try:
            girl = Girl.objects.get(domain=origin)
        except Exception:
            return HttpResponse(status=400)
        if ip:
            Guest.objects.get_or_create(ip=ip, girl=girl)
        return self._get_response(request)