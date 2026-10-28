from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from home.models import Workshop
from users.models import UserInterest
from payments.models import PaymentPlanEvent, PaymentItemType


CUSTOM_USER_FIELDS = {
    "prima_id",
    "email_confirmed",
    "allow_marketing",
    "address_1",
    "address_2",
    "legal_person_receipt",
    "legal_person_name",
    "legal_person_address_1",
    "legal_person_address_2",
    "legal_person_tax_number",
    "legal_person_vat",
    "public_profile",
    "public_username",
    "description",
    "link_1",
    "link_2",
    "link_3",
    "contact",
    "workshops_attended",
    "interests",
    "birth_date",
    "gender",
    "gender_other",
    "gallery",
    "organization",
}


class CustomUserEditForm(UserEditForm):
    prima_id = forms.IntegerField(required=False, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))
    interests = forms.ModelMultipleChoiceField(required=False, queryset=UserInterest.objects, widget=forms.CheckboxSelectMultiple, label=_("Kategorije zanimanj"))
    birth_date = forms.DateField(required=False, label=_("Datum rojstva"), widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta(UserEditForm.Meta):
        fields = UserEditForm.Meta.fields | CUSTOM_USER_FIELDS

    @property
    def memberships(self):
        return self.instance.memberships.filter(active=True).order_by('-valid_to')
    
    @property
    def subscriptions(self):
        subscription = PaymentPlanEvent.objects.filter(
            payment__user=self.instance,
            valid_to__isnull=False,
            payment_item_type=PaymentItemType.UPORABNINA,
        ).order_by('-valid_to')
        return subscription


class CustomUserCreationForm(UserCreationForm):
    prima_id = forms.IntegerField(required=False, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))
    interests = forms.ModelMultipleChoiceField(required=False, queryset=UserInterest.objects, widget=forms.CheckboxSelectMultiple, label=_("Kategorije zanimanj"))
    birth_date = forms.DateField(required=False, label=_("Datum rojstva"), widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields | CUSTOM_USER_FIELDS
