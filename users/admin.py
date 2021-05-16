from django.contrib import admin

from django.contrib.admin import register

from users.models import Profile


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'role')
    empty_value_display = '-пусто-'
