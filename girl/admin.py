from django.contrib import admin
from .models import Girl, Link, Avatar

class LinkInline(admin.TabularInline):
    fk_name = 'girl'
    model = Link
    verbose_name = 'Ссылка'
    verbose_name_plural = 'Ссылки на девочку'

class AvatarInline(admin.TabularInline):
    fk_name = 'girl'
    model = Avatar
    verbose_name = 'Аватар'
    verbose_name_plural = 'Настройка слайдера'

@admin.register(Girl)
class GirlAdmin(admin.ModelAdmin):
    list_display = ['nickname']
    prepopulated_fields = {'slug': ('nickname',)}
    inlines = [LinkInline, AvatarInline]

admin.site.site_header = "Deviant Girl'sss"
admin.site.site_title = "Deviant Girl'sss"