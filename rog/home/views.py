from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView

from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

from home.forms import RegisterForm, RegistrationMembershipForm, RegistrationInformationForm, RegistrationProfileForm

from users.models import User, Membership
from users.prima_api import PrimaApi

prima_api = PrimaApi()


@method_decorator(login_required, name='dispatch')
class MyProfileView(TemplateView):
    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        prima_user_id = current_user.prima_id
        # print(f"Prima user ID: {prima_user_id}")

        # osnovni podatki o uporabniku - zaenkrat ne rabimo nič od tega
        # user_data, message = prima_api.readUsers(prima_user_id)

        # stanje na računu uporabnika
        user_balance = prima_api.readUserBalances(prima_user_id)

        user_type = "ROG član/ica" if current_user.membership else "brezplačni uporabnik"
        obnovitev_clanarine = current_user.membership.end_day if current_user.membership else None

        return render(request, self.template_name, { 
            'user': current_user, 
            'user_balance': user_balance,
            # 'user_data': user_data,
            'user_type': user_type,
            'obnovitev_clanarine': obnovitev_clanarine
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
        users = User.objects.all() # TODO: spremeni to v filtrirane UserProfile objekte, ko extendaš Userja
        return render(request, self.template_name, {'users': users})


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

            user = User.objects.create_user(
                email=email,
                password=password,
                is_active=True
            )

            login(request, user)

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

        form = RegistrationMembershipForm()
        return render(request, "registration/registration_2_membership.html", context={ "form": form })
    
    def post(self, request):
        user = request.user
        form = RegistrationMembershipForm(request.POST)

        if form.is_valid():
            membership_choice = form.cleaned_data["membership_choice"]

            if membership_choice == "with-membership":
                today = date.today()
                one_year_from_now = today + relativedelta(years=1)
                user.membership = Membership(start_day=today, end_day=one_year_from_now)
                user.membership.save()
                user.save()

            return redirect("registration-information")
        else:
            return render(request, "registration/registration_2_membership.html", context={ "form": form })

@method_decorator(login_required, name='dispatch')
class RegistrationInformationView(View):

    def get(self, request):
        user = request.user

        form = RegistrationInformationForm()
        return render(request, "registration/registration_3_information.html", context={ "form": form })
    
    def post(self, request):
        user = request.user
        form = RegistrationInformationForm(request.POST)

        if form.is_valid():
            address_1 = form.cleaned_data["address_1"]
            address_2 = form.cleaned_data["address_2"]

            user.address_1 = address_1 # TODO: throw error if there is no address 1
            # TODO: save address_2, if it exists
            user.save()

            return redirect("registration-profile")
        else:
            return render(request, "registration/registration_3_information.html", context={ "form": form })


@method_decorator(login_required, name='dispatch')
class RegistrationProfileView(View):

    def get(self, request):
        user = request.user

        form = RegistrationProfileForm()
        return render(request, "registration/registration_4_profile.html", context={ "form": form })
    
    def post(self, request):
        user = request.user
        form = RegistrationProfileForm(request.POST)

        if form.is_valid():
            public_profile = form.cleaned_data["public_profile"]
            public_username = form.cleaned_data["public_username"]
            description = form.cleaned_data["description"]
            link = form.cleaned_data["link"]

            user.public_profile = public_profile
            user.public_username = public_username
            user.description = description
            user.link = link

            user.save()

            return redirect("registration-payment")
        else:
            return render(request, "registration/registration_4_profile.html", context={ "form": form })
    
    # def post(self, request):
        # create PRIMA user
        # data, message = prima_api.createUser(first_name, last_name, username, email, phone)
        # print(data)

        # if data:
        #     prima_id = data['UsrID']
        #     user = User.objects.create_user(
        #         username=username,
        #         first_name=first_name,
        #         last_name=last_name,
        #         email=email,
        #         phone=phone,
        #         password=password,
        #         prima_id=int(prima_id),
        #         is_active=True
        #     ) # TODO: spremeni is_active na False, ko bo treba nekoč še potrditveni mail poslat
        #     print("Novi user", user)


@method_decorator(login_required, name='dispatch')
class RegistrationPaymentView(View):

    def get(self, request):
        user = request.user

        # TODO: payment logika
        
        return render(request, "registration/registration_5_payment.html", context={ "user": user })


@method_decorator(login_required, name='dispatch')
class RegistrationSuccessView(View):

    def get(self, request):
        return render(request, "registration/registration_6_success.html")
