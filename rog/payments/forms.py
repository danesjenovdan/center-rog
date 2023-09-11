from django import forms
from django.utils.translation import gettext_lazy as _


class PromoCodeForm(forms.Form):
    promo_code = forms.CharField(
        widget=forms.TextInput(attrs={"class": "p-2 me-3"}),
        label=_("Vnesi kodo za popust"),
        label_suffix="",
        required=False
    )
    payment_id = forms.CharField()
    registration = forms.BooleanField(required=False)
