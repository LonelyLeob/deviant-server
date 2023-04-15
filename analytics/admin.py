from django.contrib import admin
from .models import Geo, Mark, Source
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
import json

@admin.register(Geo)
class GeoAdmin(admin.ModelAdmin):
    list_display = ['country', 'city']
    change_list_template = 'change_list_geo.html'

    def changelist_view(self, request, extra_context=None):
        chart_data = (
            Geo.objects.values('country').annotate(requests=Count('country')).filter(requests__gte=1/4*Geo.objects.all().count())
        )
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        return super().changelist_view(request, extra_context)

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['app']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortcut', 'description']