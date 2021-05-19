from django.contrib import admin
from users.admin import StaffRequiredAdminMixin
from .models import City


class CityAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'is_primary',)
    search_fields = ('name',)
    list_filter = ('is_primary',)
    empty_field = '--- пусто ---'


admin.site.register(City, CityAdmin)
