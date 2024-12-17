from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from events.models import EventRegistration, EventRegistrationChild
from home.forms import SplitInputDateWidget


class EventRegisterPersonForm(forms.ModelForm):
    # to do: comment out
    # register_child_check = forms.BooleanField(
    #     label=_("na dogodek prijavljam otroka"), label_suffix="", required=False
    # )

    def get_deletion_widget(self):
        return forms.HiddenInput(attrs={"class": "deletion"})

    class Meta:
        model = EventRegistration
        fields = ["name", "surname", "phone"]
        # fields = ["name", "surname", "phone", "register_child_check"]
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
        label=_("Opremo v delavnicah bom uporabljal_a na lastno odgovornost."),
        label_suffix="",
        required=False,
    )

    allow_photos = forms.BooleanField(
        label=_(
            "Dovoljujem fotografiranje in snemanje izključno za potrebe promocije programa Centra Rog."
        ),
        label_suffix="",
        required=False,
    )

    class Meta:
        model = EventRegistration
        fields = ["agreement_responsibility", "allow_photos"]


class EventRegistrationChildForm(forms.ModelForm):
    child_name = forms.CharField(
        label=_("Ime otroka"),
        label_suffix="",
        required=True,
    )
    child_surname = forms.CharField(
        label=_("Priimek otroka"),
        label_suffix="",
        required=True,
    )
    parent_phone = forms.CharField(
        label=_("Telefonska številka zakonitega skrbnika"),
        label_suffix="",
        required=True,
    )
    birth_date = forms.DateField(
        label=_("Datum rojstva"),
        label_suffix="",
        widget=SplitInputDateWidget(
            attrs={"class": "select-date"}, years=range(1900, timezone.now().year)
        ),
        required=True,
    )
    gender = forms.ChoiceField(
        label=_("Spol"),
        label_suffix="",
        choices=(("F", _("ženski")), ("M", _("moški")), ("O", _("drugo"))),
        initial="",
        widget=forms.RadioSelect(attrs={"class": "gender-radio"}),
    )
    gender_other = forms.CharField(
        label=_("izpolni"),
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "spol"}),
    )

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
        widgets = {
            "child_name": forms.TextInput(),
            "child_surname": forms.TextInput(),
            "parent_phone": forms.TextInput(),
        }
