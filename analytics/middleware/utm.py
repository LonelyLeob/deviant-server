from django.http import HttpRequest
from ..models import Source, Mark


class SimpleMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest):
        app = request.GET.get('app')
        if app:
            if Source.objects.filter(shortcut=app).exists():
                source = Source.objects.get(shortcut=app)
                mark = Mark.objects.get(app=source)
                mark.requests_counter+=1
                mark.save()
            else:
                if not Source.objects.filter(name='Не опознано').exists():
                    source = Source.objects.create(name='Не опознано',
                                                description='Пользователь подключился из неопознанного источника',
                                                shortcut='-')
                    source.save()
                    mark = Mark.objects.get(app=source)
                    mark.requests_counter+=1
                    mark.save()
                else:
                    source = Source.objects.get(name='Не опознано')
                    mark = Mark.objects.get(app=source)
                    mark.requests_counter+=1
                    mark.save()
        else:
            if not Source.objects.filter(name='Напрямую').exists():
                source = Source.objects.create(name='Напрямую', description='Пользователь подключился напрямую',
                                            shortcut='-')
                source.save()
                mark = Mark.objects.get(app=source)
                mark.requests_counter+=1
                mark.save()
            else:
                source = Source.objects.get(name='Напрямую')
                mark = Mark.objects.get(app=source)
                mark.requests_counter+=1
                mark.save()
        return self._get_response(request)

    def _process_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip