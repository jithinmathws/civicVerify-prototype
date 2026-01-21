from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ("email",)
    list_display = ("email", "is_staff")

    fieldsets = (
        (None, {"fields": ("email", "username", "full_name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "full_name", "password1", "password2"),
        }),
    )