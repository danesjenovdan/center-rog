from users.models import User, Membership
from payments.models import PaymentPlanEvent
from users.prima_api import PrimaApi

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Daily check and update of prima groups based on expired memberships and subscriptions"

    def handle(self, *args, **options):
        prima_api = PrimaApi()
        
        # Preveri vse uporabnike, ki imajo nastavljen prima_group_id
        users_with_groups = User.objects.exclude(prima_group_id__isnull=True)
        
        for user in users_with_groups:
            # Preveri aktivno članarino (group 100)
            active_membership = Membership.objects.filter(
                user=user,
                valid_to__gte=timezone.now(),
                active=True,
            ).first()
            
            # Preveri aktivno uporabnino (group 101 ali 102)
            active_subscription = PaymentPlanEvent.objects.filter(
                user=user,
                valid_to__gte=timezone.now(),
                plan__event_payment_item_type=PaymentPlanEvent.PaymentItemType.UPORABNINA,
            ).order_by('-valid_to').first()  # trenutno aktivna uporabnina
            
            correct_group_id = None
            
            # Logika določanja pravilne skupine:
            # 1. Če ima aktivno uporabnino (101 ali 102), mora imeti tudi članarino
            if active_subscription:
                if active_membership:
                    # Ima uporabnino in članarino -> nastavi skupino uporabnine
                    correct_group_id = active_subscription.plan.prima_group_id
                else:
                    # Ima uporabnino, ampak nima članarine -> odstrani iz skupine
                    correct_group_id = None
            # 2. Če ima samo članarino brez uporabnine
            elif active_membership:
                correct_group_id = 100
            # 3. Če nima nič -> odstrani iz skupine
            else:
                correct_group_id = None
            
            # Posodobi skupino, če se je spremenila
            if user.prima_group_id != correct_group_id:
                if correct_group_id is not None:
                    # Nastavi novo skupino
                    prima_api.addUserToSubscriptionGroup(user.prima_id, correct_group_id)
                    user.prima_group_id = correct_group_id
                    user.save()
                    self.stdout.write(f"User {user.email} set to group {correct_group_id}")
                else:
                    # Odstrani iz trenutne skupine
                    prima_api.removeUserFromSubscriptionGroup(user.prima_id, user.prima_group_id)
                    user.prima_group_id = None
                    user.save()
                    self.stdout.write(f"User {user.email} removed from group (no active membership/subscription)")
        
        self.stdout.write(self.style.SUCCESS('Prima groups daily reset completed'))