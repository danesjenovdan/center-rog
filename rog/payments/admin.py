from django.contrib import admin
from .models import Plan, Payment, PromoCode

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

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_to', 'percent_discount', 'item_type', 'single_use', 'number_of_uses']
    list_filter = ('item_type', 'single_use',)

    readonly_fields = ['created_at', 'updated_at']


    def get_changeform_initial_data(self, request):
        return {'code': 'custom_initial_value'}