from django.contrib import admin
from .models import Human

@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ['country', 'city']