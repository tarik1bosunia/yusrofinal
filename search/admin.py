from django.contrib import admin
from search.models import Name


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
