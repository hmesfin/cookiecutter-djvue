from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced admin interface for User model."""
    
    list_display = [
        "username",
        "email",
        "full_name",
        "is_verified_badge",
        "is_active",
        "is_staff",
        "created_at",
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
        "created_at",
        "updated_at",
    ]
    search_fields = ["username", "email", "first_name", "last_name", "phone_number"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": ("first_name", "last_name", "email", "phone_number", "date_of_birth")
        }),
        (_("Profile"), {
            "fields": ("bio", "avatar"),
            "classes": ("collapse",),
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_verified",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined", "created_at", "updated_at"),
        }),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "is_verified",
            ),
        }),
    )
    
    readonly_fields = ["created_at", "updated_at", "date_joined", "last_login"]
    
    def full_name(self, obj):
        """Display user's full name."""
        return obj.get_full_name() or "-"
    full_name.short_description = _("Full Name")
    
    def is_verified_badge(self, obj):
        """Display verification status as a badge."""
        if obj.is_verified:
            return format_html(
                '<span style="color: green;">✓ Verified</span>'
            )
        return format_html(
            '<span style="color: gray;">✗ Unverified</span>'
        )
    is_verified_badge.short_description = _("Verified")
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch_related for ManyToMany fields."""
        qs = super().get_queryset(request)
        return qs.prefetch_related("groups", "user_permissions")
    
    actions = ["verify_users", "unverify_users"]
    
    def verify_users(self, request, queryset):
        """Mark selected users as verified."""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} user(s) marked as verified.")
    verify_users.short_description = _("Mark selected users as verified")
    
    def unverify_users(self, request, queryset):
        """Mark selected users as unverified."""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} user(s) marked as unverified.")
    unverify_users.short_description = _("Mark selected users as unverified")