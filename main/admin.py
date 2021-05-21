from django.contrib import admin
from main.models import Main
from users.utils import AdminAndModerMixin


class MainAdmin(AdminAndModerMixin, admin.ModelAdmin):
    list_display = (
        'event',
        'on_view'
    )
    empty_value_display = '-пусто-'


admin.site.register(Main, MainAdmin)
