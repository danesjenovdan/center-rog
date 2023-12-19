from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import EventCategory, EventRegistration


class EventCategoryAdmin(ModelAdmin):
    model = EventCategory
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


class EventRegistrationAdmin(ModelAdmin):
    model = EventRegistration
    menu_icon = "pilcrow"
    menu_order = 300
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_filter = ("register_child_check", "registration_finished")
    search_fields = ("event__title", "name", "surname", "user__first_name", "user__last_name")


modeladmin_register(EventCategoryAdmin)
modeladmin_register(EventRegistrationAdmin)
