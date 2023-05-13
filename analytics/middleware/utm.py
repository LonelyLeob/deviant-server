from django.core.handlers.wsgi import WSGIRequest
from ..models import Source, Mark
from .simple import SimpleMiddleware


class UTMMiddleware(SimpleMiddleware):
    def __call__(self, request: WSGIRequest):
        response = self._get_response(request)
        app = request.GET.get('app')
        if app:
            if Source.objects.filter(shortcut=app).exists():
                source = Source.objects.get(shortcut=app)
                mark, _ = Mark.objects.get_or_create(app=source)
                mark.requests_counter+=1
                mark.save()
            else:
                if not Source.objects.filter(name='Не опознано').exists():
                    source = Source.objects.create(name='Не опознано',
                                                description='Пользователь подключился из неопознанного источника',
                                                shortcut='-')
                    source.save()
                    mark, _ = Mark.objects.get_or_create(app=source)
                    mark.requests_counter+=1
                    mark.save()
                else:
                    source = Source.objects.get(name='Не опознано')
                    mark, _ = Mark.objects.get_or_create(app=source)
                    mark.requests_counter+=1
                    mark.save()
        else:
            if "admin" in request.get_full_path():
                return response
            if not Source.objects.filter(name='Напрямую').exists():
                source = Source.objects.create(name='Напрямую', description='Пользователь подключился напрямую',
                                            shortcut='-')
                source.save()
                mark, _ = Mark.objects.get_or_create(app=source)
                mark.requests_counter+=1
                mark.save()
            else:
                source = Source.objects.get(name='Напрямую')
                mark, _ = Mark.objects.get_or_create(app=source)
                mark.requests_counter+=1
                mark.save()
        return response