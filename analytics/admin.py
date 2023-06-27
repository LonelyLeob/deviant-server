from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from .models import GeoCounter, Mark, Source, Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['ip', 'visited_at']
    search_fields = ['girl__nickname']
    list_filter = ['girl', ('visited_at', DateRangeFilter)]

@admin.register(GeoCounter)
class GeoAdmin(admin.ModelAdmin):
    list_display = ['country', 'requests_counter']
    search_fields = ['girl__nickname', 'country']
    list_filter = ['girl']


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['app', 'requests_counter']
    search_fields = ['girl__nickname', 'app']
    list_filter = ['girl',]


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortcut', 'description']
