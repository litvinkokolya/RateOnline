from django.contrib import admin
from django import forms
from .models import *


def _meta(row):
    return ','.join([x.name for x in row.meta.all()])


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'cat', '_meta')
    list_display_links = ('id', 'first_name')
    search_fields = ('first_name', 'last_name', 'phone_number')


class RefereeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'cat', '_meta')
    list_display_links = ('id', 'first_name')
    search_fields = ('first_name', 'last_name', 'phone_number')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)


class NominationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', '_meta')
    list_display_links = ('name',)


class AtributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'nom')
    list_display_links = ('name',)


class WorkAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom')


class ScoreAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selected_work = self.instance.work_id
        print(selected_work)
        if selected_work:
            self.fields['atrib'].queryset = Atribute.objects.filter(nom_id=selected_work)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    form = ScoreAdminForm
    list_display = ('value', 'ref', 'work', 'atrib')


admin.site.register(User, UserAdmin)
admin.site.register(Referee, RefereeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Nominations, NominationsAdmin)
admin.site.register(Atribute, AtributeAdmin)
admin.site.register(Work, WorkAdmin)