from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from .models import BookingToken, MembershipType, UserInterest, MembershipTypeSpecification
from .views import ExportMarketningUsersView


class BookingTokenAdmin(ModelAdmin):
    model = BookingToken
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_display = ('email', 'token',)
    search_fields = ('email',)


class MembershipTypeAdmin(ModelAdmin):
    model = MembershipType
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


class UserInterestAdmin(ModelAdmin):
    model = UserInterest
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


class MembershipTypeSpecificationAdmin(ModelAdmin):
    model = MembershipTypeSpecification
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
        path('mailchimp_export/', ExportMarketningUsersView.as_view(), name='mailchimp_export'),
    ]


@hooks.register('register_admin_menu_item')
def register_calendar_menu_item():
    return MenuItem(_('Export for Mailchimp'), reverse('mailchimp_export'), icon_name='download')


# modeladmin_register(BookingTokenAdmin)
modeladmin_register(MembershipTypeAdmin)
modeladmin_register(UserInterestAdmin)
modeladmin_register(MembershipTypeSpecificationAdmin)
