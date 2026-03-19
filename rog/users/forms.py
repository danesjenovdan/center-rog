from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from home.models import Workshop
from users.models import UserInterest
from payments.models import PaymentPlanEvent, PaymentItemType


class CustomUserEditForm(UserEditForm):
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))
    interests = forms.ModelMultipleChoiceField(required=False, queryset=UserInterest.objects, widget=forms.CheckboxSelectMultiple, label=_("Kategorije zanimanj"))

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
    prima_id = forms.IntegerField(required=True, label=_("Prima ID"))
    workshops_attended = forms.ModelMultipleChoiceField(required=False, queryset=Workshop.objects, widget=forms.CheckboxSelectMultiple, label=_("Opravljena usposabljanja"))
    interests = forms.ModelMultipleChoiceField(required=False, queryset=UserInterest.objects, widget=forms.CheckboxSelectMultiple, label=_("Kategorije zanimanj"))
