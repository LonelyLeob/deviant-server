from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Girl, Link

class LinkInline(admin.TabularInline):
    fk_name = 'girl'
    model = Link

@admin.register(Girl)
class GirlAdmin(admin.ModelAdmin):
    list_display = ['nickname']
    prepopulated_fields = {'slug': ('nickname',)}
    inlines = [LinkInline,]

admin.site.unregister(User)
admin.site.unregister(Group)