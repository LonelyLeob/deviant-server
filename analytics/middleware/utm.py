from django.core.handlers.wsgi import WSGIRequest
from ..models import Source, Mark
from girl.models import Girl
from .simple import SimpleMiddleware


class UTMMiddleware(SimpleMiddleware):
    def __call__(self, request: WSGIRequest):
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