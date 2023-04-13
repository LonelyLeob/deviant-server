from django.http import HttpResponseRedirect, HttpRequest
from .models import Mark, Source
from girl.models import Girl

def set_utm_and_redirect(request: HttpRequest):
    app = request.GET.get('app')
    source = Source.objects.get(name=app)
    Mark.objects.create(app=source).save()
    girl_slug = request.GET.get('your_girl')
    if not girl_slug:
        return HttpResponseRedirect("https://"+"yankawildy.fun")
    girl_domain = Girl.objects.filter(slug=girl_slug).first().domain
    if girl_domain:
        return HttpResponseRedirect("https://"+girl_domain)