from django.contrib import admin
from django.db.models import Sum
from apps.contributors.models import Contributor, ReputationLog

@admin.register(ReputationLog)
class ReputationLogAdmin(admin.ModelAdmin):
    list_display = (
        "contributor",
        "change",
        "reason",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "contributor__display_name",
        "reason",
    )
    ordering = ("-created_at",)

    readonly_fields = (
        "contributor",
        "change",
        "reason",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "user",
        "reputation_score",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = (
        "display_name",
        "user__email",
    )
    ordering = ("-reputation_score",)

    readonly_fields = (
        "user",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Identity", {
            "fields": ("user", "display_name", "bio")
        }),
        ("Status", {
            "fields": ("is_active", "reputation_score")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

    actions = ["activate_contributors", "deactivate_contributors"]


@admin.action(description="Activate selected contributors")
def activate_contributors(self, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected contributors")
def deactivate_contributors(self, request, queryset):
    queryset.update(is_active=False)


def user_email(self, obj):
    return obj.user.email

user_email.short_description = "User Email"

