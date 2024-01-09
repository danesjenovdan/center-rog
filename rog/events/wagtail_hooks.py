from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import EventPage, EventCategory, EventRegistration


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


class EventRegistrationAdmin(ModelAdmin):
    model = EventRegistration
    menu_icon = "pilcrow"
    menu_order = 300
    add_to_settings_menu = True
    add_to_admin_menu = False
    list_filter = (
        "register_child_check",
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


modeladmin_register(EventCategoryAdmin)
modeladmin_register(EventRegistrationAdmin)
