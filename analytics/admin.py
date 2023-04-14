from django.contrib import admin
from .models import Geo, Mark, Source

@admin.register(Geo)
class GeoAdmin(admin.ModelAdmin):
    list_display = ['country', 'city']

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['app']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortcut','description']