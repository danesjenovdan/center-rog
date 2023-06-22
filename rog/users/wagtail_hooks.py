from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import BookingToken


class BookingTokenAdmin(ModelAdmin):
    model = BookingToken
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_display = ('email', 'token',)
    search_fields = ('email',)


modeladmin_register(BookingTokenAdmin)
