from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget

from users.models import User

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class NominationAttributeInline(admin.TabularInline):
    model = NominationAttribute


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    formfield_overrides = {models.JSONField: {"widget": JSONEditorWidget}}
    inlines = [NominationAttributeInline]


@admin.register(NominationAttribute)
class NominationAttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


class MemberNominationInline(admin.TabularInline):
    model = MemberNomination


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberNominationInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["user"].queryset = User.objects.filter(is_staff=False)
        return form


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryNomination)
class CategoryNominationAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberNomination)
class MemberNominationAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "category_nomination")
    list_display_links = ("id", "member", "category_nomination")
    ordering = ["id"]


@admin.register(MemberNominationPhoto)
class MemberNominationPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "member_nomination", "photo")
    list_display_links = ("id", "member_nomination", "photo")
    ordering = ["member_nomination"]


@admin.register(EventStaff)
class EventStaffAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category_nomination")
    list_display_links = ("id", "user", "category_nomination")
    ordering = ["user"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventStaffAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["user"].queryset = User.objects.filter(is_staff=True)
        return form


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "eventstaff", "score", "membernomination")
    list_display_links = ("id", "eventstaff", "score", "membernomination")
    ordering = ["eventstaff"]


admin.site.site_title = "Админ-панель BeautyRank"
admin.site.site_header = "Админ-панель BeautyRank"
