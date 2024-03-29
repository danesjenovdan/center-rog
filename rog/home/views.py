from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta

from home.forms import (
    RegisterForm,
    RegistrationMembershipForm,
    RegistrationInformationForm,
    EditProfileForm,
    UserInterestsForm,
    PurchasePlanForm,
)

from users.models import User, Membership, MembershipType, ConfirmEmail
from users.prima_api import PrimaApi
from users.tokens import get_token_for_user
from home.email_utils import send_email, id_generator

from payments.models import Plan
from events.models import EventRegistration

prima_api = PrimaApi()


@method_decorator(login_required, name="dispatch")
class MyProfileView(TemplateView):
    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        prima_user_id = current_user.prima_id
        # print(f"Prima user ID: {prima_user_id}")

        location_id = None
        if "location" in request.GET:
            location_id = request.GET.get("location")
        group_id = None
        if "group" in request.GET:
            group_id = request.GET.get("group")

        try:
            obnovitev_clanarine = current_user.membership.valid_to
        except AttributeError:
            obnovitev_clanarine = None

        # upcoming events
        today = date.today()
        event_registrations = EventRegistration.objects.filter(
            Q(event__start_day__gte=today) | Q(event__end_day__gte=today),
            user=current_user,
            registration_finished=True,
        )

        return render(
            request,
            self.template_name,
            {
                "user": current_user,
                "ulagtoken": get_token_for_user(current_user),
                "obnovitev_clanarine": obnovitev_clanarine,
                "location_id": location_id,
                "group_id": group_id,
                "event_registrations": event_registrations,
            },
        )


class UserProfileView(TemplateView):
    template_name = "registration/user_profile.html"

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            return render(request, self.template_name, {"user": user})
        except:
            return HttpResponseNotFound("User not found.")


@method_decorator(login_required, name="dispatch")
class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user
        return render(request, self.template_name, {"user": current_user})


@method_decorator(login_required, name="dispatch")
class SearchProfileView(TemplateView):
    template_name = "registration/search_profile.html"

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(public_profile=True)

        form = UserInterestsForm()

        return render(request, self.template_name, {"users": users, "form": form})

    def post(self, request):
        form = UserInterestsForm(request.POST)

        if form.is_valid():
            interests = form.cleaned_data["interests"]
            users = User.objects.filter(public_profile=True, interests__in=interests)
        else:
            print("Form ni valid")

        return render(request, self.template_name, {"users": users, "form": form})


@method_decorator(login_required, name="dispatch")
class PurchasePlanView(TemplateView):
    template_name = "registration/user_purchase_plan.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        form = PurchasePlanForm()
        membership_plans = MembershipType.objects.filter(
            plan__isnull=False
        ).values_list("plan", flat=True)
        form.fields["plans"].queryset = (
            Plan.objects.all().exclude(id__in=membership_plans).order_by("price")
        )

        return render(request, self.template_name, {"user": current_user, "form": form})

    def post(self, request):
        form = PurchasePlanForm(request.POST)
        membership_plans = MembershipType.objects.filter(
            plan__isnull=False
        ).values_list("plan", flat=True)
        form.fields["plans"].queryset = (
            Plan.objects.all().exclude(id__in=membership_plans).order_by("price")
        )

        if form.is_valid():
            plan = form.cleaned_data["plans"]

            return redirect(f"/placilo?plan_id={plan.id}&purchase_type=plan")
        else:
            print("Form ni valid")

        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class PurchaseMembershipView(TemplateView):
    template_name = "registration/user_purchase_membership.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        form = RegistrationMembershipForm()
        membership_types = MembershipType.objects.all().order_by(
            F("plan__price").desc(nulls_last=False)
        )

        return render(
            request,
            self.template_name,
            {"user": current_user, "form": form, "membership_types": membership_types},
        )

    def post(self, request):
        user = request.user
        membership_types = MembershipType.objects.all().order_by(
            F("plan__price").desc(nulls_last=False)
        )

        form = RegistrationMembershipForm(request.POST)

        if form.is_valid():
            membership_type = form.cleaned_data["type"]
            today = datetime.now()
            one_year_from_now = today + timedelta(days=365)
            # create membership
            if membership_type.plan:
                membership = Membership(
                    valid_from=today,
                    valid_to=one_year_from_now,
                    type=membership_type,
                    active=False,
                    user=user,
                )
                membership.save()

            if membership_type.plan:
                return redirect(
                    f"/placilo?plan_id={membership_type.plan.id}&purchase_type=membership&membership={membership.id}"
                )
            else:
                return redirect("profile-my")
        else:
            return render(
                request,
                self.template_name,
                context={"form": form, "membership_types": membership_types},
            )


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "registration/registration.html", context={"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # create PRIMA user
            data, message = prima_api.createUser(email)
            print(data)

            if data:
                prima_id = data["UsrID"]
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    prima_id=int(prima_id),
                    is_active=True,  # TODO: spremeni is_active na False, ko bo treba nekoč še potrditveni mail poslat
                )

                # tukaj pošljemo mail za potrditev računa
                # najprej naredimo ConfirmEmail objekt in generiramo ključ
                not_unique = True
                while not_unique:
                    key_gen = id_generator(size=32)
                    not_unique = ConfirmEmail.objects.filter(key=key_gen)
                confirm_email = ConfirmEmail(user=user, key=key_gen)
                confirm_email.save()
                # potem pošljemo mail
                send_email(
                    user.email,
                    "emails/email_confirmation.html",
                    _("Center Rog – potrdite račun"),
                    {"key": confirm_email.key},
                )

                login(request, user)
            else:
                print(
                    "Prišlo je do napake pri ustvarjanju novega uporabnika na Prima sistemu."
                )
                return render(
                    request,
                    "registration/registration.html",
                    context={
                        "form": form,
                        "error": _("Uporabnika ni bilo mogoče ustvariti."),
                    },
                )

            return redirect("registration-email-confirmation")
        else:
            return render(
                request, "registration/registration.html", context={"form": form}
            )


class RegistrationMailConfirmationView(View):
    def get(self, request):
        
        return render(
            request,
            "registration/registration_mail_confirmation.html",
        )


@method_decorator(login_required, name="dispatch")
class RegistrationMembershipView(View):
    def get(self, request):
        user = request.user
        membership_types = MembershipType.objects.all().order_by(
            F("plan__price").desc(nulls_last=False)
        )
        # TODO: prefill form če memberhsip že obstaja
        form = RegistrationMembershipForm()
        return render(
            request,
            "registration/registration_2_membership.html",
            context={
                "form": form,
                "registration_step": 1,
                "membership_types": membership_types,
            },
        )

    def post(self, request):
        user = request.user
        membership_types = MembershipType.objects.all().order_by(
            F("plan__price").desc(nulls_last=False)
        )

        form = RegistrationMembershipForm(request.POST)

        if form.is_valid():
            membership_type = form.cleaned_data["type"]
            today = datetime.now()
            one_year_from_now = today + timedelta(days=365)
            if membership_type.plan:
                new_membership = Membership(
                    valid_from=today,
                    valid_to=one_year_from_now,
                    type=membership_type,
                    active=False,
                    user=user,
                )
                new_membership.save()
                membership_query = f"?membership={new_membership.id}"
            else:
                membership_query = ""

            return redirect(f"/registracija/podatki{membership_query}")
        else:
            return render(
                request,
                "registration/registration_2_membership.html",
                context={
                    "form": form,
                    "registration_step": 1,
                    "membership_types": membership_types,
                },
            )


@method_decorator(login_required, name="dispatch")
class RegistrationInformationView(View):
    def get(self, request):
        user = request.user
        membership = request.GET.get("membership", None)

        form = RegistrationInformationForm(instance=user, membership=membership)
        return render(
            request,
            "registration/registration_3_information.html",
            context={"form": form, "registration_step": 2},
        )

    def post(self, request):
        user = request.user
        form = RegistrationInformationForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.address_1 = form.cleaned_data["address_1"]
            user.address_2 = form.cleaned_data["address_2"]
            user.birth_date = form.cleaned_data["birth_date"]

            gender = form.cleaned_data["gender"]
            user.gender = gender
            if gender == "O":
                user.gender_other = form.cleaned_data["gender_other"]
            else:
                user.gender_other = ""

            legal_person_receipt = form.cleaned_data["legal_person_receipt"]
            user.legal_person_receipt = legal_person_receipt
            if legal_person_receipt:
                user.legal_person_name = form.cleaned_data["legal_person_name"]
                user.legal_person_address_1 = form.cleaned_data[
                    "legal_person_address_1"
                ]
                user.legal_person_address_2 = form.cleaned_data[
                    "legal_person_address_2"
                ]
                user.legal_person_tax_number = form.cleaned_data[
                    "legal_person_tax_number"
                ]
                user.legal_person_vat = form.cleaned_data["legal_person_vat"]
            else:
                user.legal_person_name = ""
                user.legal_person_address_1 = ""
                user.legal_person_address_2 = ""
                user.legal_person_tax_number = ""
                user.legal_person_vat = False

            user.save()

            membership = form.cleaned_data["membership"]
            if membership:
                membership_query = f"?membership={membership}"
            else:
                membership_query = ""

            # prepare valid from and to dates
            valid_from = datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
            valid_to = valid_from
            # update PRIMA user
            data, message = prima_api.updateUser(
                user_id=user.prima_id,
                name=user.first_name,
                last_name=user.last_name,
                valid_from=valid_from,
                valid_to=valid_to,
            )

            return redirect(f"/registracija/profil{membership_query}")
        else:
            return render(
                request,
                "registration/registration_3_information.html",
                context={"form": form, "registration_step": 2},
            )


@method_decorator(login_required, name="dispatch")
class RegistrationProfileView(View):
    def get(self, request):
        user = request.user
        membership = request.GET.get("membership", None)
        form = EditProfileForm(instance=user, membership=membership)

        payment_needed = True if membership else False

        return render(
            request,
            "registration/registration_4_profile.html",
            context={
                "form": form,
                "registration_step": 3,
                "payment_needed": payment_needed,
            },
        )

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST)

        payment_needed = True if request.POST.get("membership", None) else False

        if form.is_valid():
            public_profile = form.cleaned_data["public_profile"]
            public_username = form.cleaned_data["public_username"]
            description = form.cleaned_data["description"]
            link_1 = form.cleaned_data["link_1"]
            link_2 = form.cleaned_data["link_2"]
            link_3 = form.cleaned_data["link_3"]
            contact = form.cleaned_data["contact"]

            User = get_user_model()
            if public_username:
                public_username_exists = (
                    User.objects.filter(public_username=public_username)
                    .exclude(id=user.id)
                    .exists()
                )
                if public_username_exists:
                    form.add_error("public_username", _("Uporabniško ime že obstaja."))

            # if public username error added
            if not form.is_valid():
                return render(
                    request,
                    "registration/registration_4_profile.html",
                    context={
                        "form": form,
                        "registration_step": 3,
                        "payment_needed": payment_needed,
                    },
                )

            user.public_profile = public_profile
            user.public_username = public_username
            user.description = description
            user.link_1 = link_1
            user.link_2 = link_2
            user.link_3 = link_3
            user.contact = contact

            user.save()
            payment_needed = user.most_recent_membership_is_billable

            membership = form.cleaned_data["membership"]
            if membership:
                membership_query = f"&membership={membership}"
            else:
                membership_query = ""

            if payment_needed:
                plan_id = user.memberships.last().type.plan.id
                return redirect(
                    f"/placilo?plan_id={plan_id}&purchase_type=registration{membership_query}"
                )
            else:
                return redirect("profile-my")
        else:
            return render(
                request,
                "registration/registration_4_profile.html",
                context={
                    "form": form,
                    "registration_step": 3,
                    "payment_needed": payment_needed,
                },
            )


@method_decorator(login_required, name="dispatch")
class EditProfileView(View):
    def get(self, request):
        user = request.user

        form = EditProfileForm(instance=user)
        return render(request, "registration/edit_profile.html", context={"form": form})

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST, request.FILES)

        if form.is_valid():
            public_profile = form.cleaned_data["public_profile"]
            public_username = form.cleaned_data["public_username"]
            description = form.cleaned_data["description"]
            link_1 = form.cleaned_data["link_1"]
            link_2 = form.cleaned_data["link_2"]
            link_3 = form.cleaned_data["link_3"]
            contact = form.cleaned_data["contact"]
            interests = form.cleaned_data["interests"]

            User = get_user_model()
            if public_username:
                public_username_exists = (
                    User.objects.filter(public_username=public_username)
                    .exclude(id=user.id)
                    .exists()
                )
                if public_username_exists:
                    form.add_error("public_username", _("Uporabniško ime že obstaja."))

            if not form.is_valid():
                return render(
                    request, "registration/edit_profile.html", context={"form": form}
                )

            user.public_profile = public_profile
            user.public_username = public_username
            user.description = description
            user.link_1 = link_1
            user.link_2 = link_2
            user.link_3 = link_3
            user.contact = contact

            for interest in interests:
                user.interests.add(interest)

            user.save()

            return redirect("profile-my")
        else:
            return render(
                request, "registration/edit_profile.html", context={"form": form}
            )


# @method_decorator(login_required, name='dispatch')
# class RegistrationPaymentView(View):

#     def get(self, request):
#         user = request.user

#         # TODO: payment logika

#         return render(request, "registration/registration_5_payment.html", context={ "user": user })


# @method_decorator(login_required, name='dispatch')
# class RegistrationSuccessView(View):

#     def get(self, request):
#         return render(request, "registration/registration_6_success.html")
