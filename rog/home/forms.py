from django import forms
from django.forms import widgets
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    # email = forms.CharField(widget=widgets.EmailInput, label='E-naslov')
    # password = forms.CharField(widget=widgets.PasswordInput, label='Geslo')
    # newsletter_permission = forms.BooleanField(
    #     label="Newsletter",
    #     label_suffix='',
    #     required=False
    # )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            # 'newsletter_permission'
        ]
