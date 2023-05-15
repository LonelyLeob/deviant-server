from ..models import Source, Mark
from girl.models import Girl
from .simple import SimpleMiddleware, IPMiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist


class UTMMiddleware(SimpleMiddleware, IPMiddlewareMixin):
    def __call__(self, request):
        response = self._get_response(request)
        app = request.GET.get('app')
        origin = request.headers.get('Origin')
        if "admin" in request.get_full_path():
            return response
        if not origin:
            return response
        if app:
            if Source.objects.filter(shortcut=app).exists():
                source = Source.objects.get(shortcut=app)
                try:
                    girl = Girl.objects.get(domain=origin)
                except:
                    girl = None                
                mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
                mark.requests_counter+=1
                mark.save()
            else:
                if not Source.objects.filter(name='Не опознано').exists():
                    try:
                        girl = Girl.objects.get(domain=origin)
                    except:
                        girl = None
                    source = Source.objects.create(name='Не опознано',
                                                description='Пользователь подключился из неопознанного источника',
                                                shortcut='-',)
                    source.save()
                    mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
                    mark.requests_counter+=1
                    mark.save()
                else:
                    try:
                        girl = Girl.objects.get(domain=origin)
                    except:
                        girl = None
                    source = Source.objects.get(name='Не опознано')
                    mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
                    mark.requests_counter+=1
                    mark.save()
        else:
            if not Source.objects.filter(name='Напрямую').exists():
                try:
                    girl = Girl.objects.get(domain=origin)
                except:
                    girl = None
                source = Source.objects.create(name='Напрямую', description='Пользователь подключился напрямую',
                                            shortcut='-')
                source.save()
                mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
                mark.requests_counter+=1
                mark.save()
            else:
                try:
                    girl = Girl.objects.get(domain=origin)
                except:
                    girl = None
                source = Source.objects.get(name='Напрямую')
                mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
                mark.requests_counter+=1
                mark.save()
        return response
    
class MarkMiddleware(SimpleMiddleware, IPMiddlewareMixin):
    def __call__(self, request):
        if "admin" in request.get_full_path():
            return self._get_response(request)
        app, origin = request.GET.get('app'), request.headers.get('Origin')
        if origin:
            try:
                girl = Girl.objects.get(domain=origin)
            except Exception:
                return self._get_response()
            if app:
                try:
                    source = Source.objects.get(name=app)
                except ObjectDoesNotExist:
                    source = Source.objects.create(name="Не опознано", shortcut="-", description="Неопознанное приложение")
            source, created = Source.objects.get_or_create(name="Напрямую")
            if created:
                source.shortcut, source.description = "-", "Заход без приложения"
                source.save()
            mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
            mark.requests_counter+=1
            mark.save()
        return self._get_response(request)