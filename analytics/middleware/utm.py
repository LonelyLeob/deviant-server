from ..models import Source, Mark
from girl.models import Girl
from .simple import SimpleMiddleware, IPMiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist, BadRequest


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
                raise BadRequest
            if app:
                try:
                    source = Source.objects.get(shortcut=app)
                except ObjectDoesNotExist:
                    source = Source.objects.get_or_create(name="Не опознано", shortcut="-", description="Неопознанное приложение")
            else:
                try:
                    source = Source.objects.get(name="Напрямую")
                except ObjectDoesNotExist:
                    source = Source.objects.create(name="Напрямую", shortcut="-", description="Пользователь подключился напрямую")
            mark, _ = Mark.objects.get_or_create(app=source, girl=girl)
            mark.requests_counter+=1
            mark.save()
        return self._get_response(request)