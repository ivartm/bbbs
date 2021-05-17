from django.contrib import admin
from django.contrib.admin import register

from .models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_primary',)
    search_fields = ('name',)
    list_filter = ('is_primary',)
    empty_field = '--- пусто ---'


admin.site.register(City, CityAdmin)
