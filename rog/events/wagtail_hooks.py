from django.contrib.admin import SimpleListFilter
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q, Count, OuterRef, Subquery
from django.urls import path, reverse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.menu import MenuItem
from wagtail import hooks
from wagtail_rangefilter.filters import DateRangeFilter
from users.prima_api import PrimaApi

from .models import EventPage, EventCategory, EventRegistration
from .views import event_list
from .export import ExportModelAdminMixin
from payments.models import PaymentPlanEvent

prima_api = PrimaApi()

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
            return queryset.filter(event=self.value())


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
    list_display = [
        "__str__",
        "registration_finished",
        "get_children_count",
        "get_extra_people_count",
        "created_at",
        "updated_at",
        "original_event_name",
        "price_paid_online",
    ]
    list_filter = (
        "register_child_check",
        "event__event_is_for_children",
        "registration_finished",
        # "event__start_day",
        ("event__start_day", DateRangeFilter),
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
        plan_name = Subquery(
            PaymentPlanEvent.objects.filter(
                event_registration=OuterRef("id"),
            ).values(
                "plan_name"
            )[:1]
        )
        paid = Subquery(
            PaymentPlanEvent.objects.filter(
                event_registration=OuterRef("id"),
            ).values(
                "price"
            )[:1]
        )
        qs = qs.annotate(
            booked_children=Count("event_registration_children"),
            booked_extra_people=Count("event_registration_extra_people"),
            original_name=plan_name,
            paid=paid,
        )
        return qs

    def get_children_count(self, obj):
        return obj.booked_children

    def get_extra_people_count(self, obj):
        return obj.booked_extra_people

    def original_event_name(self, obj):
        return obj.original_name

    def price_paid_online(self, obj):
        return obj.paid

    get_children_count.__name__ = str(_("Število otrok"))
    get_extra_people_count.__name__ = str(_("Število dodatnih oseb"))


@csrf_protect
def grant_event_ability_form_view(request):
    """View showing form to select registrations for granting workshop"""
    if request.method == "POST":
        registration_ids = request.POST.getlist("registration_ids")
        updated_count = 0

        for registration_id in registration_ids:
            try:
                registration = EventRegistration.objects.get(id=registration_id)
                print("Workshop", registration.event.event_is_workshop)
                if registration.event.event_is_workshop:
                    registration.user.workshops_attended.add(
                        registration.event.event_is_workshop
                    )
                    prima_api.addUserToGroup(
                        registration.user.prima_id, registration.event.event_is_workshop.prima_id
                    )
                    updated_count += 1
            except EventRegistration.DoesNotExist:
                print(f"Registration with id {registration_id} does not exist.")
                continue

        messages.success(
            request,
            _("Usposabljanje je bilo dodano {} udeležencem.").format(updated_count),
        )

        # Redirect back to admin list with filters if they exist
        query_string = request.POST.get("query_string", "")
        if query_string:
            return redirect(f"/admin/events/eventregistration/?{query_string}")
        else:
            return redirect("/admin/events/eventregistration/")

    # GET request - show form
    registrations = EventRegistration.objects.select_related("event", "user").filter(
        registration_finished=True
    )

    # Apply filters from query string (same filters as EventRegistrationAdmin)
    # Filter by relevant event
    if event_id := request.GET.get("relevant_event"):
        registrations = registrations.filter(event_id=event_id)

    # Filter by event__event_is_for_children
    if event_is_for_children := request.GET.get("event__event_is_for_children"):
        registrations = registrations.filter(
            event__event_is_for_children=event_is_for_children
        )

    # Filter by register_child_check
    if register_child_check := request.GET.get("register_child_check"):
        registrations = registrations.filter(register_child_check=register_child_check)

    # Filter by registration_finished
    if registration_finished := request.GET.get("registration_finished"):
        registrations = registrations.filter(
            registration_finished=registration_finished
        )

    # Filter by event__start_day range (DateRangeFilter)
    # Format: event__start_day__range_from=YYYY-MM-DD&event__start_day__range_to=YYYY-MM-DD
    if range_from := request.GET.get("event__start_day__range_from"):
        registrations = registrations.filter(event__start_day__gte=range_from)

    if range_to := request.GET.get("event__start_day__range_to"):
        registrations = registrations.filter(event__start_day__lte=range_to)

    registrations = registrations.order_by("-created_at")

    context = {
        "registrations": registrations,
        "title": _("Dodaj usposabljanje udeležencem"),
        "query_string": request.GET.urlencode(),
    }

    return render(request, "events/grant_ability_form.html", context)


@hooks.register("register_admin_urls")
def register_eventlist_url():
    return [
        path("event_list/", event_list, name="event_list"),
        path("grant_ability/", grant_event_ability_form_view, name="grant_ability"),
    ]


@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    return MenuItem("Prihajajoči dogodki", reverse("event_list"), icon_name="date")


modeladmin_register(EventCategoryAdmin)
modeladmin_register(EventRegistrationAdmin)
