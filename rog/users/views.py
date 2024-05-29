from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from home import models
from home.email_utils import send_email, id_generator
from users.models import ConfirmEmail
from .tokens import get_email_for_token, get_token_for_user


class CheckTokenView(View):
    def get(self, request):
        if token := request.GET.get("whoistoken", ""):
            if email := get_email_for_token(token):
                return HttpResponse(f"OK|{email}")
        return HttpResponse("ERROR|Invalid token")


@method_decorator(login_required, name='dispatch')
class TestCalendarTemplateView(TemplateView):
    template_name = "users/test_calendar.html"

    def get(self, request, *args, **kwargs):
        current_user = request.user
        return render(request, self.template_name, {
            'user': current_user,
            'ulagtoken': get_token_for_user(current_user),
        })


@method_decorator(login_required, name='dispatch')
class EditGalleryView(View):
    def get(self, request):
        current_user = request.user
        print(current_user.gallery.raw_data)
        print(type(current_user.gallery))
        return JsonResponse({"message": "GET OK", "user": current_user.id})

    def post(self, request):
        current_user = request.user

        uploaded_images = request.FILES.getlist('image')
        new_images = []

        new_gallery = []

        for image in current_user.gallery:
            print(image.value)
            new_gallery.append(("image", image.value))

        for uploaded_file in uploaded_images:
            image = models.CustomImage(title=uploaded_file.name, file=uploaded_file)
            image.save()
            image.tags.add("__user_gallery__")
            new_gallery.append(('image', image))
            new_images.append({
                'id': image.id,
                'src': image.file.url
            })

        current_user.gallery = new_gallery
        current_user.save()

        return JsonResponse({"message": "POST OK", "images": new_images})


@method_decorator(login_required, name='dispatch')
class DeleteGalleryView(View):

    def post(self, request):
        current_user = request.user

        image_id = request.POST.get("id", None)

        try:
            new_gallery = []

            for image in current_user.gallery:
                if image.value.id != int(image_id):
                    new_gallery.append(("image", image.value))

            current_user.gallery = new_gallery
            current_user.save()

            return JsonResponse({"message": "DELETE OK"})

        except:
            return HttpResponseBadRequest()


class ResendConfirmationMailView(View):
    def get(self, request):
        user = request.user
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

        return redirect("registration-email-confirmation")


class ConfirmUserView(View):
    def get(self, request):
        key = request.GET.get("key", None)
        print("key confirm user", key)
        confirm_email = get_object_or_404(ConfirmEmail, key=key)
        user = confirm_email.user
        user.email_confirmed = True
        user.save()
        confirm_email.delete()
        send_email(
            user.email,
            "emails/registration.html",
            _(
                "Center Rog – vaša registracija je uspela // your registration was successful"
            )
        )
        return redirect("registration-membership")
