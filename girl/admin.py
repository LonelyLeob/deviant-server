from django.contrib import admin
from .models import Girl, Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['link']

@admin.register(Girl)
class GirlAdmin(admin.ModelAdmin):
    list_display = ['nickname']
    prepopulated_fields = {'slug': ('nickname',)}