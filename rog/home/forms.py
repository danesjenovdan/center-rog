from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django.db import ProgrammingError
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import User, MembershipType, Membership, UserInterest
from payments.models import Plan


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_check = cleaned_data.get("password_check")

        if password and len(password) < 8:
            self.add_error("password", _("Geslo mora biti dolgo vsaj 8 znakov."))
        if password and not any(char.isdigit() for char in password):
            self.add_error("password", _("Geslo mora vsebovati vsaj eno številko."))

        if password != password_check:
            self.add_error("password", _("Gesli se ne ujemata."))
            self.add_error("password_check", _("Gesli se ne ujemata."))

        return cleaned_data

    class Meta:
        model = User
        fields = [
            "email",
            "newsletter",
            "password",
            "password_check"
        ]


class RegistrationMembershipForm(forms.ModelForm):
    # try:
    #     membership_types = [ (mt.id, mt.name) for mt in MembershipType.objects.all() ]
    # except ProgrammingError: # ta exception je treba dat, ker MembershipType še ne obstaja v bazi, ko se prvič požene projekt
    #     membership_types = []
    # membership_choice = forms.ChoiceField(required=True, choices=membership_types, widget=forms.RadioSelect)

    class Meta:
        model = Membership
        fields = [
            "type",
        ]
        widgets = {
            "type": forms.RadioSelect(),
        }


class SplitInputDateWidget(forms.SelectDateWidget):
    input_type = "number"
    select_widget = forms.NumberInput

    def get_context(self, name, value, attrs):
        context = super(forms.SelectDateWidget, self).get_context(name, value, attrs)
        date_context = {}
        year_name = self.year_field % name
        date_context["year"] = self.select_widget(
            attrs,
        ).get_context(
            name=year_name,
            value=context["widget"]["value"]["year"],
            attrs={**context["widget"]["attrs"], "id": "id_%s" % year_name, "placeholder": "1989"},
        )
        month_name = self.month_field % name
        date_context["month"] = self.select_widget(
            attrs,
        ).get_context(
            name=month_name,
            value=context["widget"]["value"]["month"],
            attrs={**context["widget"]["attrs"], "id": "id_%s" % month_name, "placeholder": "12"},
        )
        day_name = self.day_field % name
        date_context["day"] = self.select_widget(
            attrs,
        ).get_context(
            name=day_name,
            value=context["widget"]["value"]["day"],
            attrs={**context["widget"]["attrs"], "id": "id_%s" % day_name, "placeholder": "31"},
        )
        subwidgets = []
        for field in self._parse_date_fmt():
            subwidgets.append(date_context[field]["widget"])
        context["widget"]["subwidgets"] = subwidgets
        return context


class RegistrationInformationForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Ime"),
        label_suffix="",
    )
    last_name = forms.CharField(
        label=_("Priimek"),
        label_suffix="",
    )
    birth_date = forms.DateField(
        label=_("Datum rojstva"),
        label_suffix="",
        widget=SplitInputDateWidget(attrs={"class": "select-date"}, years=range(1900, timezone.now().year)),
        required=True
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
        widget=forms.TextInput(attrs={"placeholder": "spol"})
    )
    address_1 = forms.CharField(
        label=_("Naslov 1"),
        label_suffix="",
    )
    address_2 = forms.CharField(
        label=_("Naslov 2 (neobvezno)"),
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
    legal_person_tax_number = forms.IntegerField(
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

    membership = forms.CharField(
        widget=forms.HiddenInput(),
        required = False
    )

    def clean_legal_person_tax_number(self):
        legal_person_receipt = self.cleaned_data["legal_person_receipt"]
        legal_person_tax_number = self.cleaned_data["legal_person_tax_number"]
        if legal_person_receipt and not legal_person_tax_number:
            raise ValidationError(_("Pravna oseba mora vnesti davčno številko!"))

        return legal_person_tax_number

    def __init__(self, *args, **kwargs):
        self.membership = kwargs.pop("membership", None)
        super().__init__(*args, **kwargs)
        if self.membership:
            self.initial['membership'] = self.membership

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "gender_other",
            "address_1",
            "address_2",
            "legal_person_receipt",
            "legal_person_name",
            "legal_person_address_1",
            "legal_person_address_2",
            "legal_person_tax_number",
            "legal_person_vat"
        ]

class EditProfileForm(forms.ModelForm):
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
    link_1 = forms.URLField(
        label=_("Dodaj povezavo do svoje spletne strani ali profila na družabnem omrežju"),
        label_suffix="",
        required=False
    )
    link_2 = forms.URLField(
        label=_("Dodaj povezavo do svoje spletne strani ali profila na družabnem omrežju"),
        label_suffix="",
        required=False
    )
    link_3 = forms.URLField(
        label=_("Dodaj povezavo do svoje spletne strani ali profila na družabnem omrežju"),
        label_suffix="",
        required=False
    )
    contact = forms.EmailField(
        label=_("Kontakt"),
        label_suffix="",
        required=False
    )
    interests = forms.ModelMultipleChoiceField(
        required=False,
        queryset=UserInterest.objects,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "radio"})
    )
    gallery = forms.Field(
        required=False,
    )
    custom_gallery = MultipleFileField(required=False)

    membership = forms.CharField(
        widget=forms.HiddenInput(),
        required = False
    )

    def __init__(self, *args, **kwargs):
        self.membership = kwargs.pop("membership", None)
        super().__init__(*args, **kwargs)
        if self.membership:
            self.initial['membership'] = self.membership

    class Meta:
        model = User
        fields = [
            "public_profile",
            "public_username",
            "description",
            "link_1",
            "link_2",
            "link_3",
            "contact",
            "interests",
            "gallery",
        ]


class UserInterestsForm(forms.Form):
    interests = forms.ModelMultipleChoiceField(
        required=False,
        queryset=UserInterest.objects,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "radio"})
    )


class PurchasePlanForm(forms.Form):
    plans = forms.ModelChoiceField(
        required=True,
        queryset=Plan.objects,
        widget=forms.RadioSelect(attrs={"class": "radio"})
    )
