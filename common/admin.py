from django.contrib import admin
from django.contrib.admin import register

from common.models import City

@register(City)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_primary')
    empty_value_display = '-пусто-'
