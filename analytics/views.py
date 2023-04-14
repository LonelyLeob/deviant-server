from django.http import HttpRequest, HttpResponse
from .models import Mark, Source

def set_utm(request: HttpRequest):
    app = request.GET.get('app')
    if app:
        if Source.objects.filter(shortcut=app).exists():
            source = Source.objects.get(shortcut=app)
            Mark.objects.create(app=source).save()
        else:
            if not Source.objects.filter(name='Не опознано').exists():
                source = Source.objects.create(name='Не опознано', description='Пользователь подключился из неопознанного источника', shortcut='-')
                source.save()
                Mark.objects.create(app=source).save()
            else:
                source = Source.objects.filter(name='Не опознано').first()
                Mark.objects.create(app=source).save()
    else:
        if not Source.objects.filter(name='Напрямую').exists():
            source = Source.objects.create(name='Напрямую', description='Пользователь подключился напрямую', shortcut='-')
            source.save()
            Mark.objects.create(app=source).save()
        else:
            source = Source.objects.filter(name='Напрямую').first()
            Mark.objects.create(app=source).save()
    return HttpResponse('')