from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Workshop


class WorkshopAdmin(ModelAdmin):
    model = Workshop
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    add_to_admin_menu = False  # or False to exclude your model from the menu
    # list_display = ('title', 'author')
    # list_filter = ('author',)
    # search_fields = ('title', 'author')


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(WorkshopAdmin)


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/custom_admin.css")
    )
