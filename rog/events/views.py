from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import formset_factory


from events.models import EventPage, EventRegistration
from events.forms import (
    EventRegisterPersonForm,
    EventRegisterAdditionalForm,
    EventRegisterInformationForm,
    EventRegistrationChildForm,
)


@method_decorator(login_required, name="dispatch")
class EventRegistrationView(View):
    def get(self, request, event):
        # user
        current_user = request.user

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
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterPersonForm(instance=event_registration)
                # new registration children formset
                # TODO: treba dopolnit, če že obstajajo vezani otroci
                children_formset = formset_factory(EventRegistrationChildForm)
        except:
            # new registration form
            form = EventRegisterPersonForm(
                {"name": current_user.first_name, "surname": current_user.last_name}
            )
            # new registration children formset
            children_formset = formset_factory(EventRegistrationChildForm)

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

        # event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        try:
            event_registration = EventRegistration.objects.get(
                user=current_user, event=event
            )
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterPersonForm(
                    request.POST, instance=event_registration
                )
        except:
            form = EventRegisterPersonForm(request.POST)

        if form.is_valid():
            print("Prijavnica je valid")
            event_registration = form.save(commit=False)
            event_registration.user = current_user
            event_registration.event = event
            event_registration.save()
        else:
            print("Prijavnica ni valid")
            return render(
                request,
                "events/event_registration_2.html",
                context={"event": event, "form": form},
            )

        return redirect("event-registration-additional", event=event.slug)


@method_decorator(login_required, name="dispatch")
class EventRegistrationAdditionalView(View):
    def get(self, request, event):
        # user
        current_user = request.user

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        try:
            event_registration = EventRegistration.objects.get(
                user=current_user, event=event
            )
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterAdditionalForm(instance=event_registration)
        except:
            return redirect("event-registration", event=event.slug)

        return render(
            request,
            "events/event_registration_2.html",
            context={"form": form, "registration_step": 1, "event": event},
        )

    def post(self, request, event):
        # user
        current_user = request.user

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        try:
            event_registration = EventRegistration.objects.get(
                user=current_user, event=event
            )
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterAdditionalForm(
                    request.POST, instance=event_registration
                )
        except:
            return redirect("event-registration", event=event.slug)

        if form.is_valid():
            print("Prijavnica je valid")
            form.save()
        else:
            print("Prijavnica ni valid")

            return render(
                request,
                "events/event_registration_3.html",
                context={"form": form, "registration_step": 1, "event": event},
            )

        return redirect("event-registration-information", event=event.slug)


@method_decorator(login_required, name="dispatch")
class EventRegistrationInformationView(View):
    def get(self, request, event):
        # user
        current_user = request.user

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        try:
            event_registration = EventRegistration.objects.get(
                user=current_user, event=event
            )
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterInformationForm(instance=event_registration)
        except:
            return redirect("event-registration", event=event.slug)

        return render(
            request,
            "events/event_registration_3.html",
            context={"form": form, "registration_step": 2, "event": event},
        )

    def post(self, request, event):
        # user
        current_user = request.user

        # check for event
        try:
            event = EventPage.objects.get(slug=event)
        except:
            return redirect("profile-my")

        # update existing or return to first step
        try:
            event_registration = EventRegistration.objects.get(
                user=current_user, event=event
            )
            if event_registration.registration_finished:
                return redirect(event.get_url())
            else:
                form = EventRegisterInformationForm(
                    request.POST, instance=event_registration
                )
        except:
            return redirect("event-registration", event=event.slug)

        if form.is_valid():
            print("Prijavnica je valid")
            form.save()
        else:
            print("Prijavnica ni valid")

        # TODO: preusmeri na plačilo
        return render(
            request,
            "events/event_registration_3.html",
            context={"form": form, "registration_step": 2, "event": event},
        )
