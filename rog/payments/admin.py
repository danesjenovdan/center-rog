from django.contrib import admin
from .models import Plan, Payment

# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'valid_from', 'valid_to']
    list_filter = ()

    readonly_fields = ['created_at', 'updated_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'amount', 'created_at']
    list_filter = ('status', 'items')

    readonly_fields = ['created_at', 'updated_at']
