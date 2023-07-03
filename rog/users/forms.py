from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from home.models import Workshop
from users.models import UserInterest


class CustomUserEditForm(UserEditForm):
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))
    interests = forms.ModelMultipleChoiceField(required=False, queryset=UserInterest.objects, widget=forms.CheckboxSelectMultiple, label=_("Kategorije zanimanj"))


class CustomUserCreationForm(UserCreationForm):
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))
    interests = forms.ModelMultipleChoiceField(required=False, queryset=UserInterest.objects, widget=forms.CheckboxSelectMultiple, label=_("Kategorije zanimanj"))

