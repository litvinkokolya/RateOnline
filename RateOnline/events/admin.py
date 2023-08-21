from django.contrib import admin

from users.models import User
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class NominationAttributeInline(admin.TabularInline):
    model = NominationAttribute


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    inlines = [NominationAttributeInline]


@admin.register(NominationAttribute)
class NominationAttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].queryset = User.objects.filter(is_staff=False)
        return form


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryNomination)
class CategoryNominationAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberNomination)
class MemberNominationAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'category_nomination', 'photo_1')
    list_display_links = ('id', 'member', 'category_nomination')
    ordering = ['id']


@admin.register(WinnerNomination)
class WinnerNominationAdmin(admin.ModelAdmin):
    pass


@admin.register(WinnerCategory)
class WinnerCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(EventStaff)
class EventStaffAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(EventStaffAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].queryset = User.objects.filter(is_staff=True)
        return form


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass


admin.site.site_title = 'Админ-панель BeautyRank'
admin.site.site_header = 'Админ-панель BeautyRank'
