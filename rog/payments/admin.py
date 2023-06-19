from django.contrib import admin
from .models import Plan

# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'valid_from', 'valid_to']
    list_filter = ()

    readonly_fields = ['created_at', 'updated_at']
