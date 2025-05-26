import ast

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
    def __init__(self, *args, **kwargs):
        extra_questions_values = kwargs.pop("extra_questions_values")
        super().__init__(*args, **kwargs)

        field_order = []
        for i, item in enumerate(extra_questions_values):
            field_name = f"extra_question_{i}"
            field_order.append(field_name)
            if item["type"] == "text":
                self.fields[field_name] = forms.CharField(
                    label=item["question"],
                    required=item["required"],
                    widget=forms.TextInput(),
                )
                if item.get("initial", None):
                    self.initial[field_name] = item["initial"]
            elif item["type"] == "textarea":
                self.fields[field_name] = forms.CharField(
                    label=item["question"],
                    required=item["required"],
                    widget=forms.Textarea(),
                )
                if item.get("initial", None):
                    self.initial[field_name] = item["initial"]
            elif item["type"] == "radio":
                self.fields[field_name] = forms.ChoiceField(
                    label=item["question"],
                    required=item["required"],
                    choices=[(x, x) for x in item["choices"]],
                    widget=forms.RadioSelect(),
                )
                if item.get("initial", None):
                    initial_value = self._eval_initial_list(item["initial"])
                    self.initial[field_name] = initial_value
            elif item["type"] == "checkboxes":
                self.fields[field_name] = forms.MultipleChoiceField(
                    label=item["question"],
                    required=item["required"],
                    choices=[(x, x) for x in item["choices"]],
                    widget=forms.CheckboxSelectMultiple(),
                )
                if item.get("initial", None):
                    initial_value = self._eval_initial_list(item["initial"])
                    self.initial[field_name] = initial_value
            elif item["type"] == "file":
                self.fields[field_name] = forms.FileField(
                    label=item["question"],
                    required=item["required"],
                    widget=forms.ClearableFileInput(),
                )
                if item.get("initial", None):
                    self.initial[field_name] = item["initial"]

        # order the extra questions fields first (fields missing from field_order,
        # like the default defined fields will be at the end)
        self.order_fields(field_order)

    def _eval_initial_list(self, string_value):
        if string_value:
            if string_value.startswith("[") and string_value.endswith("]"):
                try:
                    value = ast.literal_eval(string_value)
                    if isinstance(value, list):
                        return value
                except (ValueError, SyntaxError):
                    pass
        return string_value

    def get_extra_questions_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith("extra_question_"):
                yield (self.fields[name].label, value)

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


class EventRegistrationExtraPersonForm(forms.ModelForm):
    person_name = forms.CharField(
        label=_("Ime osebe"),
        label_suffix="",
        required=True,
    )
    person_surname = forms.CharField(
        label=_("Priimek osebe"),
        label_suffix="",
        required=True,
    )

    class Meta:
        model = EventRegistrationChild
        fields = [
            "person_name",
            "person_surname",
        ]
        widgets = {
            "person_name": forms.TextInput(),
            "person_surname": forms.TextInput(),
        }
