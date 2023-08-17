from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Plan, Payment


class PlanAdmin(ModelAdmin):
    model = Plan
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


class PaymentAdmin(ModelAdmin):
    model = Payment
    menu_icon = "form"
    menu_order = 201
    add_to_settings_menu = True
    add_to_admin_menu = False


modeladmin_register(PlanAdmin)
modeladmin_register(PaymentAdmin)
