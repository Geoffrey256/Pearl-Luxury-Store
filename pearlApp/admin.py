from .models import Category, Product, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount",
                    "discounted_price", "stock_quantity")
    list_filter = ("category",)
    search_fields = ("name", "description")
