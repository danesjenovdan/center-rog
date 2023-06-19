from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from users.models import Membership


class CustomUserEditForm(UserEditForm):
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))


class CustomUserCreationForm(UserCreationForm):
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))

