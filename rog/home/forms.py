from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from users.models import User


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("elektronski naslov"),
        label_suffix="",
    )
    newsletter = forms.BooleanField(
        label=_("prijavi me na novičnik"),
        label_suffix="",
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label=_("geslo (vsaj 8 znakov, vsaj ena številka)"),
        label_suffix=""
    )
    password_check = forms.CharField(
        widget=forms.PasswordInput, 
        label=_("ponovi geslo"),
        label_suffix=""
    )

    class Meta:
        model = User
        fields = [
            "email",
            "newsletter",
            "password",
            "password_check"
        ]


class RegistrationMembershipForm(forms.Form):
    membership_choice = forms.ChoiceField(required=True, choices=[
        ("no-membership", "Brez članstva"), 
        ("with-membership", "S članstvom")
    ], widget=forms.RadioSelect)


class RegistrationInformationForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Ime"),
        label_suffix="",
    )
    last_name = forms.CharField(
        label=_("Priimek"),
        label_suffix="",
    )
    address_1 = forms.CharField(
        label=_("Naslov 1"),
        label_suffix="",
    )
    address_2 = forms.CharField(
        label=_("Naslov 2"),
        label_suffix="",
        required=False
    )
    legal_person_receipt = forms.BooleanField(
        label=_("potrebujem račun za pravno osebo"),
        label_suffix="",
        required=False
    )
    legal_person_name = forms.CharField(
        widget=forms.TextInput, 
        label=_("Naziv pravne osebe"),
        label_suffix="",
        required=False
    )
    legal_person_address_1 = forms.CharField(
        widget=forms.TextInput, 
        label=_("Naslov 1"),
        label_suffix="",
        required=False
    )
    legal_person_address_2 = forms.CharField(
        widget=forms.TextInput, 
        label=_("Naslov 2 (neobvezno)"),
        label_suffix="",
        required=False
    )
    legal_person_tax_number = forms.CharField(
        widget=forms.TextInput, 
        label=_("Davčna številka"),
        label_suffix="",
        required=False
    )
    legal_person_vat = forms.BooleanField(
        label=_("sem zavezanec za DDV"),
        label_suffix="",
        required=False
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "address_1",
            "address_2",
            "legal_person_receipt",
            "legal_person_name",
            "legal_person_address_1",
            "legal_person_address_2",
            "legal_person_tax_number",
            "legal_person_vat"
        ]

class RegistrationProfileForm(forms.ModelForm):    
    public_profile = forms.BooleanField(
        label=_("Spodnje informacije so lahko javne in vidne drugim uporabnikom centra Rog"),
        label_suffix="",
        required=False
    )
    public_username = forms.CharField(
        widget=forms.TextInput, 
        label=_("Uporabniško ime"),
        label_suffix="",
        required=False
    )
    description = forms.CharField(
        widget=forms.Textarea, 
        label=_("Opis"),
        label_suffix="",
        required=False
    )
    link = forms.URLField(
        label=_("Dodaj povezavo do svoje spletne strani ali profila na družabnem omrežju"),
        label_suffix=""
    )

    class Meta:
        model = User
        fields = [
            "public_profile",
            "public_username",
            "description",
            "link"
        ]

