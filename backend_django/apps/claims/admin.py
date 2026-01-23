from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.claims.models.claim import Claim, ClaimTag, ClaimStatus
from django.utils.html import format_html


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "colored_status",
        "is_public",
        "created_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "is_public", "created_at")
    search_fields = ("title", "description", "created_by__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "created_by")
    list_select_related = ("created_by",)
    date_hierarchy = "created_at"
    actions = ["make_public", "make_private"]


    fieldsets = (
        (None, {
            "fields": ("title", "description", "status", "is_public")
        }),
        (_("Ownership"), {
            "fields": ("created_by",)
        }),
        (_("Timestamps"), {
            "fields": ("created_at", "updated_at")
        }),
    )

    @admin.action(description=_("Mark selected claims as public"))
    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, _(f"{updated} claim(s) marked as public."))

    @admin.action(description=_("Mark selected claims as private"))
    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, _(f"{updated} claim(s) marked as private."))

    def colored_status(self, obj):
        color = "green" if obj.status == ClaimStatus.VERIFIED else "red"
        return format_html('<span style="color:{};">{}</span>', color, obj.status)
    colored_status.short_description = "Status"

@admin.register(ClaimTag)
class ClaimTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
