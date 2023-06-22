from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
