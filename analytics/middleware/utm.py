from ..models import Source, Mark
from girl.models import Girl
from .simple import SimpleMiddleware, IPMiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
    
class MarkMiddleware(SimpleMiddleware, IPMiddlewareMixin):
    def __call__(self, request):
        if "admin" in request.get_full_path() or "media" in request.get_full_path():
            return self._get_response(request)
        app, origin = request.GET.get('app'), request.headers.get('Origin')
        try:
            girl = Girl.objects.get(domain=origin)
        except Exception:
            return HttpResponse(content="Exception in UTM", status=400)
        if app:
            try:
                source = Source.objects.get(shortcut=app)
            except ObjectDoesNotExist:
                try:
                    source = Source.objects.get(name="Не опознано")
                except ObjectDoesNotExist:
                    source = Source.objects.create(name="Не опознано", shortcut="-", description="Неопознанное приложение")
        else:
            try:
                source = Source.objects.get(name="Напрямую")
            except ObjectDoesNotExist:
                source = Source.objects.create(name="Напрямую", shortcut="-", description="Пользователь подключился напрямую")
        mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
        mark.requests_counter+=1
        mark.save()
        return self._get_response(request)