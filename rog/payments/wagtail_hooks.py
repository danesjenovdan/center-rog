from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Plan


class PlanAdmin(ModelAdmin):
    model = Plan
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_admin_menu = True

modeladmin_register(PlanAdmin)
