from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserCreateForm
from .models import *


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    add_form = UserCreateForm
    list_display = ('last_name', 'phone_number', 'is_staff')
    list_display_links = ('last_name', 'phone_number')
    search_fields = ('last_name', 'phone_number')
    ordering = ['last_name']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", 'phone_number'),
            },
        ),
    )
    fieldsets = (
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", 'image')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
