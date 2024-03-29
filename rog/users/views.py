from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from home import models
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
