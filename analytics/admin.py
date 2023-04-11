from django.contrib import admin
from .models import Geo

@admin.register(Geo)
class GeoAdmin(admin.ModelAdmin):
    list_display = ['country', 'city']
