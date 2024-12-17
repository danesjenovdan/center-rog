from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import BookingToken, MembershipType, UserInterest


class BookingTokenAdmin(ModelAdmin):
    model = BookingToken
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_display = (
        "email",
        "token",
    )
    search_fields = ("email",)


class MembershipTypeAdmin(ModelAdmin):
    model = MembershipType
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


class UserInterestAdmin(ModelAdmin):
    model = UserInterest
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


# modeladmin_register(BookingTokenAdmin)
modeladmin_register(MembershipTypeAdmin)
modeladmin_register(UserInterestAdmin)
