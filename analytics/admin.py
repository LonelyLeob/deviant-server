from django.contrib import admin
from .models import GeoCounter, Mark, Source, Guest
from django.core.serializers.json import DjangoJSONEncoder
import json


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['ip', 'visited_at']

@admin.register(GeoCounter)
class GeoAdmin(admin.ModelAdmin):
    list_display = ['country', 'requests_counter']
    change_list_template = 'admin/change_list_geo.html'

    def changelist_view(self, request, extra_context=None):
        chart_data = (
            GeoCounter.objects.values()
        )
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {
            "chart_data": as_json,

        }
        return super().changelist_view(request, extra_context)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['app', 'requests_counter']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortcut', 'description']
