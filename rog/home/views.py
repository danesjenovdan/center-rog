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
from django.urls import reverse

from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta

from home.forms import (
    RegistrationInfoForm,
    RegistrationMembershipForm,
    EditProfileForm,
    UserInterestsForm,
    PurchasePlanForm,
)

from users.models import User, Membership, MembershipType, ConfirmEmail
from users.prima_api import PrimaApi
from users.tokens import get_token_for_user
from home.email_utils import send_email, id_generator

from payments.models import Plan, TokenSettings
from events.models import EventRegistration

prima_api = PrimaApi()


@method_decorator(login_required, name="dispatch")
class MyProfileView(TemplateView):
    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

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
        if current_user.prima_id:
            token_balance, prima_msg = prima_api.getUserTokenBalance(current_user.prima_id)
        else:
            token_balance = 0
            prima_msg = ""

        return render(
            request,
            self.template_name,
            {
                "user": current_user,
                "unused_subscriptions": current_user.get_unused_subscriptions(),
                "ulagtoken": get_token_for_user(current_user),
                "obnovitev_clanarine": obnovitev_clanarine,
                "location_id": location_id,
                "group_id": group_id,
                "event_registrations": event_registrations,
                "token_balance": token_balance,
                "token_msg": prima_msg,
            },
        )


class UserProfileView(TemplateView):
    template_name = "registration/user_profile.html"

    def get(self, request, id):
        current_user = request.user

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseNotFound("User not found.")

        if not current_user.is_anonymous and not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        if user == current_user or user.public_profile:
            return render(request, self.template_name, {"user": user})

        return HttpResponseNotFound("User not public.")


@method_decorator(login_required, name="dispatch")
class SearchProfileView(TemplateView):
    template_name = "registration/search_profile.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        users = User.objects.filter(public_profile=True)

        form = UserInterestsForm()

        return render(request, self.template_name, {"users": users, "form": form})

    def post(self, request):
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

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

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        form = PurchasePlanForm()
        membership_plans = MembershipType.objects.filter(
            plan__isnull=False
        ).values_list("plan", flat=True)
        form.fields["plans"].queryset = (
            Plan.objects.all().exclude(id__in=membership_plans).order_by("price")
        )

        return render(request, self.template_name, {"user": current_user, "form": form})

    def post(self, request):
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        form = PurchasePlanForm(request.POST)
        membership_plans = MembershipType.objects.filter(
            plan__isnull=False
        ).values_list("plan", flat=True)
        form.fields["plans"].queryset = (
            Plan.objects.all().exclude(id__in=membership_plans).order_by("price")
        )

        if form.is_valid():
            plan = form.cleaned_data["plans"]
            # get language code for redirect url
            language_code = request.LANGUAGE_CODE
            if language_code != "sl":
                language_code = f"/{language_code}"
            else:
                language_code = ""

            if plan.custom_buy_url:
                return redirect(f"{language_code}{plan.custom_buy_url}")

            return redirect(f"{language_code}/placilo?plan_id={plan.id}&purchase_type=plan")
        else:
            print("Form ni valid")

        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class PurchaseTokensView(TemplateView):
    template_name = "registration/user_purchase_tokens.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user
        token_settings = TokenSettings()

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        return render(request, self.template_name, {"user": current_user, "token_settings": token_settings})

    def post(self, request):
        current_user = request.user
        token_settings = TokenSettings()

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        request_data = request.POST
        tokens = request_data.get("token_quantity")

        if tokens:
            # get language code for redirect url
            language_code = request.LANGUAGE_CODE
            if language_code != "sl":
                language_code = f"/{language_code}"
            else:
                language_code = ""

            return redirect(f"{language_code}/placilo?&purchase_type=tokens&tokens={tokens}")
        else:
            print("Form ni valid")

        return render(request, self.template_name, {"user": current_user,  "token_settings": token_settings})


@method_decorator(login_required, name="dispatch")
class PurchaseMembershipView(TemplateView):
    template_name = "registration/user_purchase_membership.html"

    def get(self, request, extend_membership, *args, **kwargs):
        current_user = request.user

        if not current_user.email_confirmed:
            return redirect("registration-email-confirmation")

        form = RegistrationMembershipForm()
        membership_types = MembershipType.objects.all().order_by(
            F("plan__price").desc(nulls_last=None)
        )
        if extend_membership:
            membership_types = membership_types.filter(
                plan__price__gt=0
            )

        return render(
            request,
            self.template_name,
            {
                "user": current_user,
                "form": form,
                "membership_types": membership_types,
                "extend_membership": extend_membership,
            },
        )

    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.email_confirmed:
            return redirect("registration-email-confirmation")

        membership_types = MembershipType.objects.all().order_by(
            F("plan__price").desc(nulls_last=None)
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


class RegistrationChooseTypeView(TemplateView):
    template_name = "registration/registration_choose_type.html"

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get("next", None)

        membership_types = MembershipType.objects.all().order_by(
            F("plan__price").desc(nulls_last=None)
        )

        return render(
            request,
            self.template_name,
            context={
                "registration_step": 0,
                "next_page": next_page,
                "membership_types": membership_types,
            },
        )


class RegistrationInformationView(TemplateView):
    template_name = "registration/registration_information.html"

    def get(self, request, *args, **kwargs):
        type_id = request.GET.get("id", None)
        if type_id:
            try:
                membership_type = MembershipType.objects.get(id=type_id)
            except MembershipType.DoesNotExist:
                membership_type = None

        if not type_id or not membership_type:
            return redirect("registration")

        form = RegistrationInfoForm(for_membership=membership_type.plan is not None)

        return render(
            request,
            self.template_name,
            context={
                "registration_step": 1,
                "membership_type": membership_type,
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        type_id = request.GET.get("id", None)
        if type_id:
            try:
                membership_type = MembershipType.objects.get(id=type_id)
            except MembershipType.DoesNotExist:
                membership_type = None

        if not type_id or not membership_type:
            return redirect("registration")

        form = RegistrationInfoForm(request.POST, for_membership=membership_type.plan is not None)

        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                email=email,
                password=password,
                is_active=True,  # TODO: spremeni is_active na False, ko bo treba nekoč še potrditveni mail poslat
            )

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
            else:
                new_membership = None

            # # prepare valid from and to dates
            # valid_from = datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
            # valid_to = valid_from
            # # update PRIMA user
            # data, message = prima_api.updateUser(
            #     user_id=user.prima_id,
            #     name=user.first_name,
            #     last_name=user.last_name,
            #     valid_from=valid_from,
            #     valid_to=valid_to,
            # )

            # nastavi podatke za redirect nazaj po konfirmaciji
            extra_query = ""
            next = request.GET.get("next", None)
            if new_membership:
                extra_query += f"&membership={new_membership.id}"
                extra_query += f"&next=registration-profile"
            elif next:
                extra_query += f"&next={next}"

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
                "Center Rog – potrditev e-naslova // e-mail confirmation",
                {
                    "key": confirm_email.key,
                    "extra_query": extra_query
                },
            )

            login(request, user)

            return redirect(reverse("registration-email-confirmation") + f"?id={membership_type.id}")
        else:
            return render(
                request,
                self.template_name,
                context={
                    "registration_step": 1,
                    "membership_type": membership_type,
                    "form": form,
                },
            )


class RegistrationMailConfirmationView(View):
    def get(self, request):
        user = request.user
        type_id = request.GET.get("id", None)
        membership_type = None

        if type_id:
            try:
                membership_type = MembershipType.objects.get(id=type_id)
            except MembershipType.DoesNotExist:
                pass

        if user.is_authenticated and user.email_confirmed:
            membership = request.GET.get("membership", None)
            next_page = request.GET.get("next", None)

            last_membership = user.memberships.last()
            if last_membership:
                payment_needed = user.most_recent_membership_is_billable
                if membership and payment_needed:
                    if payment_needed:
                        plan_id = last_membership.type.plan.id
                        url = f"/placilo?plan_id={plan_id}&purchase_type=registration&membership={membership}"
                        if next_page:
                            url += f"&next={next_page}"
                        return redirect(url)

            if next_page:
                return redirect(next_page)

            return redirect("profile-my")

        return render(
            request,
            "registration/registration_mail_confirmation.html",
            context={
                "registration_step": 2,
                "membership_type": membership_type,
            },
        )


@method_decorator(login_required, name="dispatch")
class RegistrationProfileView(View):
    def get(self, request):
        user = request.user
        membership = request.GET.get("membership", None)
        form = EditProfileForm(instance=user, membership=membership)
        next_page = request.GET.get("next", None)

        payment_needed = True if membership else False

        return render(
            request,
            "registration/registration_4_profile.html",
            context={
                "form": form,
                "registration_step": 4,
                # this page is only for memberships so just fake that it has a plan for progress dots
                "membership_type": {"plan": True},
                "payment_needed": payment_needed,
                "next_page": next_page,
            },
        )

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST)

        payment_needed = True if request.POST.get("membership", None) else False
        next_page = request.GET.get("next", None)

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
                        "next_page": next_page,
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
                if next_page:
                    next_page = f"&next={next_page}"
                else:
                    next_page = ""
                return redirect(
                    f"/placilo?plan_id={plan_id}&purchase_type=registration{membership_query}{next_page}"
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
                    "next_page": next_page,
                },
            )


@method_decorator(login_required, name="dispatch")
class EditProfileView(View):
    def get(self, request):
        user = request.user

        if not user.email_confirmed:
            return redirect("registration-email-confirmation")

        form = EditProfileForm(instance=user)
        return render(request, "registration/edit_profile.html", context={"form": form})

    def post(self, request):
        user = request.user

        if not user.email_confirmed:
            return redirect("registration-email-confirmation")

        next_page = request.GET.get("next", None)

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

            if next_page:
                return redirect(f"{next_page}")

            return redirect("profile-my")
        else:
            return render(
                request, "registration/edit_profile.html", context={"form": form}
            )
