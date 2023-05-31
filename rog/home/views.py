from django.contrib.auth import authenticate, login
from users.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from django.views import View
from django.views.generic import TemplateView

import requests
import xmltodict

from home.forms import RegisterForm

from users.prima_api import PrimaApi

prima_api = PrimaApi()


@method_decorator(login_required, name='dispatch')
class MyProfileView(TemplateView):
    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user

        prima_user_id = current_user.prima_id

        data, message = prima_api.readUsers(prima_user_id)
        # response = prima_api.readUserBalances(prima_user_id)

        return render(request, self.template_name, { 'user': current_user, 'response': data })
    

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


class ThankYouForRegistrationView(TemplateView):
    template_name = "registration/thankyou.html"


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "registration/registration.html", context={ "form": form })

    def post(self, request):
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        # newsletter_permission = request.POST.get("newsletter_permission", False)

        # try logging the user in
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     # return redirect(redirect_path)

        # user = User.objects.create_user(
        #     username, email=username, password=password, is_active=False
        # )

        # prima api call
        data, message = prima_api.createUser(first_name, last_name, username, email, phone)
        print(data)

        if data:
            prima_id = data['UsrID']

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=password,
                prima_id=int(prima_id),
                is_active=True
            ) # TODO: spremeni is_active na False, ko bo treba nekoč še potrditveni mail poslat

            print("Novi user", user)

            # Newsletter(
            #     user=user, permission=True if newsletter_permission == "on" else False
            # ).save()
            # TODO send verification email
        
        return redirect("/hvala/")