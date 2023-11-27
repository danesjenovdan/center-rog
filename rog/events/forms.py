from django import forms
from django.utils.translation import gettext_lazy as _

from events.models import EventRegistration, EventRegistrationChild


class EventRegisterPersonForm(forms.ModelForm):
    register_child_check = forms.BooleanField(
        label=_("na dogodek prijavljam otroka"), label_suffix="", required=False
    )

    class Meta:
        model = EventRegistration
        fields = ["name", "surname", "phone"]
        widgets = {
            "name": forms.TextInput(),
            "surname": forms.TextInput(),
            "phone": forms.TextInput(),
        }


class EventRegisterAdditionalForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ["disabilities", "allergies"]


class EventRegisterInformationForm(forms.ModelForm):
    agreement_responsibility = forms.BooleanField(
        label=_("strinjam se z zavrnitvijo odgovornosti"),
        label_suffix="",
        required=False,
    )

    allow_photos = forms.BooleanField(
        label=_("dovoljujem, da me Center Rog fotografira in snema:"),
        label_suffix="",
        required=False,
    )

    class Meta:
        model = EventRegistration
        fields = ["agreement_responsibility", "allow_photos"]


class EventRegistrationChildForm(forms.ModelForm):
    class Meta:
        model = EventRegistrationChild
        fields = [
            "child_name",
            "child_surname",
            "parent_phone",
            "birth_date",
            "gender",
            "gender_other",
        ]
