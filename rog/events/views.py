from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, Count, F, Q

from datetime import datetime

from events.models import EventPage, EventRegistration, EventRegistrationChild
from events.forms import (
    EventRegisterPersonForm,
    EventRegisterAdditionalForm,
    EventRegisterInformationForm,
    EventRegistrationChildForm,
)


@method_decorator(login_required, name="dispatch")
class EventRegistrationView(View):
    ChildrenFormset = modelformset_factory(
        EventRegistrationChild,
        form=EventRegistrationChildForm,
        fields=[
            "child_name",
            "child_surname",
            "parent_phone",
            "birth_date",
            "gender",
            "gender_other",
        ],
        can_delete=True,
        min_num=1,
        extra=0,
        validate_min=True,
    )

    def get(self, request, event):
        # user
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        # event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # make sure registration event doesn't already exist
        try:
            event_registration = EventRegistration.objects.get(
                user=current_user, event=event
            )
            event_registration_children = EventRegistrationChild.objects.filter(
                event_registration=event_registration
            )
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterPersonForm(instance=event_registration)
                # new registration children formset
                children_formset = self.ChildrenFormset(
                    queryset=event_registration_children
                )

        except:
            # new registration form
            form = EventRegisterPersonForm(
                {"name": current_user.first_name, "surname": current_user.last_name}
            )
            # new registration children formset
            children_formset = self.ChildrenFormset(
                queryset=EventRegistrationChild.objects.none()
            )

        return render(
            request,
            "events/event_registration_1.html",
            context={
                "event": event,
                "form": form,
                "children_formset": children_formset,
            },
        )

    def post(self, request, event):
        # user
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        # event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        event_registration = EventRegistration.objects.filter(
            user=current_user, event=event
        ).first()

        # event registration object already exists
        if event_registration:
            # event registration is already finished -> return to event
            if event_registration.registration_finished:
                return redirect(event.get_url())
            # event registration is not finished yet -> use the existing object
            else:
                form = EventRegisterPersonForm(
                    request.POST, instance=event_registration
                )
        else:
            form = EventRegisterPersonForm(request.POST)

        children_formset = self.ChildrenFormset(
            request.POST,
            error_messages={"too_few_forms": _("Prosimo, dodajte vsaj enega otroka.")},
        )

        if form.is_valid():
            # user registration
            if not event.event_is_for_children:
                if not form.cleaned_data.get("name"):
                    form.add_error("name", _("To polje ne sme biti prazno."))
                if not form.cleaned_data.get("surname"):
                    form.add_error("surname", _("To polje ne sme biti prazno."))
                if not form.cleaned_data.get("phone"):
                    form.add_error("phone", _("To polje ne sme biti prazno."))

                if form.is_valid():
                    event_registration = form.save(commit=False)
                    event_registration.user = current_user
                    event_registration.event = event
                    event_registration.save()

                else:
                    return render(
                        request,
                        "events/event_registration_1.html",
                        context={
                            "event": event,
                            "form": form,
                            "children_formset": children_formset,
                        },
                    )

            else:
                event_registration = form.save(commit=False)
                event_registration.user = current_user
                event_registration.event = event
                event_registration.save()

                if children_formset.is_valid():
                    children = children_formset.save(commit=False)
                    for child in children:
                        child.event_registration = event_registration
                    children = children_formset.save()
                    # is there enough free places
                    registered_children = (
                        event_registration.event_registration_children.all().count()
                    )
                    free_places = event.get_free_places()
                    if registered_children > free_places:
                        return render(
                            request,
                            "events/event_registration_1.html",
                            context={
                                "event": event,
                                "form": form,
                                "children_formset": children_formset,
                                "children_formset_error": _("Na voljo ni dovolj prostih mest.")
                            },
                        )
                else:
                    return render(
                        request,
                        "events/event_registration_1.html",
                        context={
                            "event": event,
                            "form": form,
                            "children_formset": children_formset,
                        },
                    )

        else:
            # user form has errors
            return render(
                request,
                "events/event_registration_1.html",
                context={
                    "event": event,
                    "form": form,
                    "children_formset": children_formset,
                },
            )

        return redirect("event-registration-additional", event=event.slug)


@method_decorator(login_required, name="dispatch")
class EventRegistrationAdditionalView(View):
    def get(self, request, event):
        # user
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        event_registration = EventRegistration.objects.filter(
            user=current_user, event=event
        ).first()

        if event_registration:
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterAdditionalForm(instance=event_registration)
        else:
            return redirect("event-registration", event=event.slug)

        return render(
            request,
            "events/event_registration_2.html",
            context={"form": form, "registration_step": 1, "event": event},
        )

    def post(self, request, event):
        # user
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        event_registration = EventRegistration.objects.filter(
            user=current_user, event=event
        ).first()

        if event_registration:
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterAdditionalForm(
                    request.POST, instance=event_registration
                )
        else:
            return redirect("event-registration", event=event.slug)

        if form.is_valid():
            form.save()
        else:
            print(
                "Error! Na drugem koraku form ni valid, ko bi na vsak način moral bit, ker polja niso obvezna."
            )

            return render(
                request,
                "events/event_registration_2.html",
                context={"form": form, "registration_step": 1, "event": event},
            )

        return redirect("event-registration-information", event=event.slug)


@method_decorator(login_required, name="dispatch")
class EventRegistrationInformationView(View):
    def get(self, request, event):
        # user
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        event_registration = EventRegistration.objects.filter(
            user=current_user, event=event
        ).first()

        if event_registration:
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterInformationForm(instance=event_registration)
        else:
            return redirect("event-registration", event=event.slug)

        return render(
            request,
            "events/event_registration_3.html",
            context={"form": form, "registration_step": 2, "event": event},
        )

    def post(self, request, event):
        # user
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        event_registration = EventRegistration.objects.filter(
            user=current_user, event=event
        ).first()

        if event_registration:
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterInformationForm(
                    request.POST, instance=event_registration
                )
        else:
            return redirect("event-registration", event=event.slug)

        if form.is_valid():
            if not form.cleaned_data.get("agreement_responsibility"):
                form.add_error("agreement_responsibility", _("To polje je obvezno."))
                return render(
                    request,
                    "events/event_registration_3.html",
                    context={"form": form, "registration_step": 2, "event": event},
                )
            else:
                form.save()
        else:
            print(
                "Error! Na drugem koraku form ni valid, ko bi na vsak način moral bit, ker polja niso obvezna."
            )

            return render(
                request,
                "events/event_registration_3.html",
                context={"form": form, "registration_step": 2, "event": event},
            )

        if event.price > 0:
            return redirect(
                f"/placilo?purchase_type=event&event_registration={event_registration.id}"
            )
        else:
            # is there enough free places
            people_count = event_registration.event_registration_children.all().count()
            if people_count == 0:
                people_count = 1
            free_places = event.get_free_places()
            if people_count > free_places:
                return render(
                    request,
                    "events/event_registration_failed.html",
                    context={"registration_step": 4},
                )
            else:
                event_registration.registration_finished = True
                event_registration.save()
                return redirect("profile-my")


def event_list(request):
    sort_by_palces = request.GET.get('places', False)
    sort_by_booked = request.GET.get('booked', False)
    sort_by_day = request.GET.get('day', False)
    q = request.GET.get('q', None)

    future_events = EventPage.objects.filter(
        without_registrations=False,
        start_day__gte=datetime.now().date()
    )
    if q:
        future_events = future_events.filter(title__icontains=q)

    future_events = future_events.annotate(
        booked_users=Count('event_registrations', filter=Q(event_registrations__registration_finished=True, event_registrations__event_registration_children__isnull=True)),
        booked_children=Count('event_registrations__event_registration_children', filter=Q(event_registrations__registration_finished=True)),
    ).annotate(
        booked_count=F('booked_users')+F('booked_children')
    )

    if sort_by_palces:
        order_by = 'places'
        order = '' if int(sort_by_palces) > 0 else '-'
        future_events = future_events.order_by(f'{order}number_of_places')
    elif sort_by_booked:
        order_by = 'booked'
        order = '' if int(sort_by_booked) > 0 else '-'
        future_events = future_events.order_by(f'{order}booked_count')
    elif sort_by_day:
        order_by = 'day'
        order = '' if int(sort_by_day) > 0 else '-'
        future_events = future_events.order_by(f'{order}start_day')
    else:
        order_by = ''
        order = ''
    return render(request, 'event_list_admin.html', {
        'events': future_events,
        'order_by_key': order_by,
        'order': order
    })
