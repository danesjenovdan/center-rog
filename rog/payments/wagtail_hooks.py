from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtail.admin.panels import FieldPanel
from .models import Plan, Payment, ItemType, PromoCode


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


class ItemTypeAdmin(ModelAdmin):
    model = ItemType
    menu_icon = "form"
    menu_order = 202
    add_to_settings_menu = True
    add_to_admin_menu = False

class PromoCodeAdmin(ModelAdmin):
    model = PromoCode
    menu_icon = "form"
    menu_order = 203
    add_to_settings_menu = True
    add_to_admin_menu = False


modeladmin_register(PlanAdmin)
modeladmin_register(PaymentAdmin)
modeladmin_register(ItemTypeAdmin)
modeladmin_register(PromoCodeAdmin)
