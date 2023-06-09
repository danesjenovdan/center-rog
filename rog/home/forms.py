from django import forms
from django.forms import widgets
from users.models import User


class RegisterForm(forms.ModelForm):
    # newsletter_permission = forms.BooleanField(
    #     label="Newsletter",
    #     label_suffix='',
    #     required=False
    # )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]


class RegistrationMembershipForm(forms.Form):
    membership_choice = forms.ChoiceField(required=True, choices=[
        ("no-membership", "Brez članstva"), 
        ("with-membership", "S članstvom")
    ], widget=forms.RadioSelect)


class RegistrationInformationForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = [
            "address_1",
            "address_2",
            # "phone",
        ]

class RegistrationProfileForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = [
            "public_profile",
            "public_username",
            "description",
            "link"
        ]

