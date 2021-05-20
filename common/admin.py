from django.contrib import admin
from users.utils import StaffRequiredAdminMixin
from .models import City


class CityAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'is_primary',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('is_primary',)
    empty_field = '--- пусто ---'


admin.site.register(City, CityAdmin)
