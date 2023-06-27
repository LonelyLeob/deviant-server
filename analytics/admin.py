from django.contrib import admin
from .models import GeoCounter, Mark, Source, Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['ip', 'visited_at']
    search_fields = ['girl__nickname']
    list_filter = ['girl']
    date_hierarchy = 'visited_at'

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
