from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import NewsCategory


class NewsCategoryAdmin(ModelAdmin):
    model = NewsCategory
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False

modeladmin_register(NewsCategoryAdmin)
