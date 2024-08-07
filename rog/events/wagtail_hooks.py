from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q, Count, OuterRef, Subquery
from django.urls import path, reverse
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.menu import MenuItem
from wagtail import hooks

from datetime import datetime

from .models import EventPage, EventCategory, EventRegistration
from .views import event_list
from .export import ExportModelAdminMixin
from payments.models import PaymentPlanEvent


class RelevantEventsListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Trenutni in prihodni dogodki")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "relevant_event"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        now = timezone.now()

        relevant_events = (
            EventPage.objects.filter(Q(start_day__gte=now) | Q(end_day__gte=now))
            .order_by("start_day", "start_time")
            .values_list("id", "title")
        )

        return relevant_events

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either 'all' or 'relevant')
        # to decide how to filter the queryset.

        if self.value():
            return queryset.filter(
                event=self.value()
            )


class EventCategoryAdmin(ModelAdmin):
    model = EventCategory
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = True
    add_to_admin_menu = False


class EventRegistrationAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "admin_export_header.html"
    model = EventRegistration
    menu_icon = "pilcrow"
    menu_order = 300
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_display = ["__str__", "registration_finished", "get_children_count", "created_at", "updated_at", "original_event_name", "price_paid_online"]
    list_filter = (
        "register_child_check",
        "event__event_is_for_children",
        "registration_finished",
        RelevantEventsListFilter,
    )
    search_fields = (
        "event__title",
        "name",
        "surname",
        "user__first_name",
        "user__last_name",
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        plan_name = Subquery(PaymentPlanEvent.objects.filter(
            event_registration=OuterRef("id"),
        ).values("plan_name")[:1])
        paid = Subquery(PaymentPlanEvent.objects.filter(
            event_registration=OuterRef("id"),
        ).values("price")[:1])
        qs = qs.annotate(
            booked_children=Count('event_registration_children'),
            original_name=plan_name,
            paid=paid
        )
        return qs

    def get_children_count(self, obj):
        return obj.booked_children
    
    def original_event_name(self, obj):
        return obj.original_name
    
    def price_paid_online(self, obj):
        return obj.paid

    get_children_count.__name__ = str(_('Stevilo otrok'))


@hooks.register('register_admin_urls')
def register_eventlist_url():
    return [
        path('event_list/', event_list, name='event_list'),
    ]


@hooks.register('register_admin_menu_item')
def register_calendar_menu_item():
    return MenuItem('Prihajajoči dogodki', reverse('event_list'), icon_name='date')


modeladmin_register(EventCategoryAdmin)
modeladmin_register(EventRegistrationAdmin)
