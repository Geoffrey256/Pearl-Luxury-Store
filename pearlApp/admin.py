from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'contact', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ("Personal Info", {'fields': ('contact',)}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ("Important Dates", {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'contact', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)
