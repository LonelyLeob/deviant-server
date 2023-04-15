from django.http import HttpRequest, HttpResponse
from .models import Mark, Source

def set_utm(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    app = request.GET.get('app')
    if app:
        if Source.objects.filter(shortcut=app).exists():
            source = Source.objects.get(shortcut=app)
            Mark.objects.create(app=source, ip=ip).save()
        else:
            if not Source.objects.filter(name='Не опознано').exists():
                source = Source.objects.create(name='Не опознано', description='Пользователь подключился из неопознанного источника', shortcut='-')
                source.save()
                Mark.objects.create(app=source, ip=ip).save()
            else:
                source = Source.objects.filter(name='Не опознано').first()
                Mark.objects.create(app=source, ip=ip).save()
    # else:
    #     if not Source.objects.filter(name='Напрямую').exists():
    #         source = Source.objects.create(name='Напрямую', description='Пользователь подключился напрямую', shortcut='-')
    #         source.save()
    #         Mark.objects.create(app=source, ip=ip).save()
    #     else:
    #         source = Source.objects.filter(name='Напрямую').first()
    #         Mark.objects.create(app=source, ip=ip).save()
    return HttpResponse('')