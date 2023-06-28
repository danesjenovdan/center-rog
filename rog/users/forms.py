from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from users.models import Membership
from home.models import Workshop


class CustomUserEditForm(UserEditForm):
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))


class CustomUserCreationForm(UserCreationForm):
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))

