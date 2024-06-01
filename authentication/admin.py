from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'middle_name', 'last_name', 'email', 'is_staff', 'role', 'is_superuser', 'is_active',
        'last_login', 'created_at')
    list_display_links = ['last_name', 'id']
    list_filter = ('id', 'last_name')
    fields = (
        'first_name', 'last_name', 'middle_name', 'email', 'password', 'role', 'is_staff', 'is_superuser', 'is_active')


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
