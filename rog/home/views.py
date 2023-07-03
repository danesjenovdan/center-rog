from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView

from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

from home.forms import RegisterForm, RegistrationMembershipForm, RegistrationInformationForm, EditProfileForm, UserInterestsForm, PurchasePlanForm

from users.models import User, Membership, MembershipType
from users.prima_api import PrimaApi
from users.tokens import get_token_for_user


from payments.models import Plan

prima_api = PrimaApi()


@method_decorator(login_required, name='dispatch')
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

        obnovitev_clanarine = current_user.membership.valid_to

        return render(request, self.template_name, { 
            'user': current_user,
            'ulagtoken': get_token_for_user(current_user),
            'obnovitev_clanarine': obnovitev_clanarine,
            "location_id": location_id,
            "group_id": group_id,
        })
    

class UserProfileView(TemplateView):
    template_name = "registration/user_profile.html"

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            return render(request, self.template_name, {'user': user})
        except:
            return HttpResponseNotFound("User not found.")
    

@method_decorator(login_required, name='dispatch')
class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user
        return render(request, self.template_name, {'user': current_user})
    

@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class PurchasePlanView(TemplateView):
    template_name = "registration/user_purchase_plan.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        form = PurchasePlanForm()
        membership_plans = MembershipType.objects.filter(plan__isnull=False).values_list("plan", flat=True)
        form.fields["plans"].queryset = Plan.objects.all().exclude(id__in=membership_plans)

        return render(request, self.template_name, { 'user': current_user, "form": form })
    
    def post(self, request):
        form = PurchasePlanForm(request.POST)
        membership_plans = MembershipType.objects.filter(plan__isnull=False).values_list("plan", flat=True)
        form.fields["plans"].queryset = Plan.objects.all().exclude(id__in=membership_plans)
        
        if form.is_valid():
            plan = form.cleaned_data["plans"]
            print("Chosen plan", plan)

            return redirect(f"/placilo?plan_id={plan.id}")
        else:
            print("Form ni valid")

        return render(request, self.template_name, { "form": form })


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "registration/registration.html", context={ "form": form })

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # try logging user in
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile-my")

            # create PRIMA user
            data, message = prima_api.createUser(email)
            print(data)

            if data:
                prima_id = data['UsrID']
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    prima_id=int(prima_id),
                    is_active=True # TODO: spremeni is_active na False, ko bo treba nekoč še potrditveni mail poslat
                )
                print("Novi user", user)
                login(request, user)
            else:
                print("Prišlo je do napake pri ustvarjanju novega uporabnika na Prima sistemu.")
                return render(request, "registration/registration.html", context={ "form": form, "error": _("Uporabnika ni bilo mogoče ustvariti.") })
            

            # TODO subscribe to newsletter
            # Newsletter(
            #     user=user, permission=True if newsletter_permission == "on" else False
            # ).save()

            # TODO send verification email
            
            return redirect("registration-membership")
        else:
            return render(request, "registration/registration.html", context={ "form": form })
    

@method_decorator(login_required, name='dispatch')
class RegistrationMembershipView(View):

    def get(self, request):
        user = request.user
        membership_types = MembershipType.objects.all()
        # TODO: prefill form če memberhsip že obstaja
        form = RegistrationMembershipForm()
        return render(request, "registration/registration_2_membership.html", context={ "form": form, "registration_step": 1, "membership_types": membership_types })
    
    def post(self, request):
        user = request.user
        membership_types = MembershipType.objects.all()

        form = RegistrationMembershipForm(request.POST)

        if form.is_valid():
            membership_type = form.cleaned_data["type"]
            today = datetime.now()
            one_year_from_now = today + relativedelta(years=1)
            active = membership_type.plan is None
            user.membership = Membership(valid_from=today, valid_to=one_year_from_now, type=membership_type, active=active)
            user.membership.save()
            user.save()

            return redirect("registration-information")
        else:
            return render(request, "registration/registration_2_membership.html", context={ "form": form, "registration_step": 1, "membership_types": membership_types })

@method_decorator(login_required, name='dispatch')
class RegistrationInformationView(View):

    def get(self, request):
        user = request.user

        form = RegistrationInformationForm(instance=user)
        return render(request, "registration/registration_3_information.html", context={ "form": form, "registration_step": 2 })
    
    def post(self, request):
        user = request.user
        form = RegistrationInformationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address_1 = form.cleaned_data["address_1"]
            address_2 = form.cleaned_data["address_2"]

            user.first_name = first_name
            user.last_name = last_name
            user.address_1 = address_1
            if address_2:
                user.address_2 = address_2
            
            legal_person_receipt = form.cleaned_data["legal_person_receipt"]
            if legal_person_receipt:
                
                legal_person_name = form.cleaned_data["legal_person_name"]
                legal_person_address_1 = form.cleaned_data["legal_person_address_1"]
                legal_person_address_2 = form.cleaned_data["legal_person_address_2"]
                legal_person_tax_number = form.cleaned_data["legal_person_tax_number"]
                legal_person_vat = form.cleaned_data["legal_person_vat"]

                user.legal_person_name = legal_person_name
                user.legal_person_address_1 = legal_person_address_1
                user.legal_person_address_2 = legal_person_address_2
                user.legal_person_tax_number = legal_person_tax_number
                user.legal_person_vat = legal_person_vat

            user.save()

            return redirect("registration-profile")
        else:
            return render(request, "registration/registration_3_information.html", context={ "form": form, "registration_step": 2 })


@method_decorator(login_required, name='dispatch')
class RegistrationProfileView(View):

    def get(self, request):
        user = request.user
        form = EditProfileForm(instance=user)

        plan_id = None
        payment_needed = False
        if user.membership and user.membership.type:
            payment_needed = user.membership.type.price() > 0
            if payment_needed:
                plan_id = user.membership.type.plan.id

        return render(request, "registration/registration_4_profile.html", context={ "form": form, "registration_step": 3, "payment_needed": payment_needed })
    
    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST)

        plan_id = None
        payment_needed = False
        if user.membership and user.membership.type:
            payment_needed = user.membership.type.price() > 0
            if payment_needed:
                plan_id = user.membership.type.plan.id

        if form.is_valid():
            public_profile = form.cleaned_data["public_profile"]
            public_username = form.cleaned_data["public_username"]
            description = form.cleaned_data["description"]
            link_1 = form.cleaned_data["link_1"]
            link_2 = form.cleaned_data["link_2"]
            link_3 = form.cleaned_data["link_3"]
            contact = form.cleaned_data["contact"]

            user.public_profile = public_profile
            user.public_username = public_username
            user.description = description
            user.link_1 = link_1
            user.link_2 = link_2
            user.link_3 = link_3
            user.contact = contact

            user.save()

            if payment_needed:
                return redirect(f"/placilo?plan_id={plan_id}")
            else:
                return redirect("profile-my")
        else:
            return render(request, "registration/registration_4_profile.html", context={ "form": form, "registration_step": 3, "payment_needed": payment_needed })


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):

    def get(self, request):
        user = request.user

        form = EditProfileForm(instance=user)
        return render(request, "registration/edit_profile.html", context={ "form": form })
    
    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST)

        if form.is_valid():
            public_profile = form.cleaned_data["public_profile"]
            public_username = form.cleaned_data["public_username"]
            description = form.cleaned_data["description"]
            link_1 = form.cleaned_data["link_1"]
            link_2 = form.cleaned_data["link_2"]
            link_3 = form.cleaned_data["link_3"]
            contact = form.cleaned_data["contact"]

            user.public_profile = public_profile
            user.public_username = public_username
            user.description = description
            user.link_1 = link_1
            user.link_2 = link_2
            user.link_3 = link_3
            user.contact = contact

            user.save()

            return redirect("profile-my")
        else:
            return render(request, "registration/edit_profile.html", context={ "form": form })


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
