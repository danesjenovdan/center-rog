from users.models import User, Membership
from events.models import EventCategory
from payments.models import Payment, PaymentPlanEvent
from users.prima_api import PrimaApi

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "One per day reset of prima groups for members and subscriptions"

    def handle(self, *args, **options):
        prima_api = PrimaApi()
        # Set groups for all active members
        active_memberships = Membership.objects.filter(
            valid_to__gte=timezone.now(),
            active=True,
        ).select_related("user", "plan")
        for active_membership in active_memberships:
            user = active_membership.user
            prima_api.addUserToSubscriptionGroup(user.prima_id, 100)

        # Set groups and tokens for all active payment plans
        active_subscriptions = PaymentPlanEvent.objects.filter(
            valid_to__gte=timezone.now(),
            plan__prima_group_id__isnull=False,
        ).select_related("user", "plan")
        for active_payment in active_subscriptions:
            user = active_payment.user
            plan = active_payment.plan
            prima_api.addUserToSubscriptionGroup(user.prima_id, plan.prima_group_id)
            prima_api.addTokensToUserBalance(user.prima_id, plan.tokens)

