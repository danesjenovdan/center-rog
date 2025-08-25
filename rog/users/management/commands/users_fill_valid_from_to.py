from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.prima_api import PrimaApi
from payments.models import PaymentItemType

prima_api = PrimaApi()

User = get_user_model()


class Command(BaseCommand):
    help = "Fill valid_from and valid_to on users."

    def handle(self, *args, **options):
        self.stdout.write("Start fill valid_from and valid_to on users.")

        today_midnight = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        for user in User.objects.all():
            valid_from = today_midnight
            valid_to = today_midnight

            sub_payments = user.payments.filter(
                items__payment_item_type=PaymentItemType.UPORABNINA,
                successed_at__isnull=False,
            )
            payment_plan = None
            if sub_payments:
                payment_plan = (
                    sub_payments.latest("successed_at")
                    .payment_plans.all()
                    .filter(plan__payment_item_type=PaymentItemType.UPORABNINA)
                    .last()
                )

            if payment_plan:
                valid_from = payment_plan.valid_to - timezone.timedelta(
                    days=payment_plan.plan.duration
                )
                valid_to = payment_plan.valid_to

            valid_from_prima = valid_from.strftime("%Y-%m-%d %H:%M:%S")
            valid_to_prima = valid_to.strftime("%Y-%m-%d %H:%M:%S")

            self.stdout.write(f"{user.email} - prima_id={user.prima_id}")
            self.stdout.write(f"  valid_from={valid_from_prima}")
            self.stdout.write(f"    valid_to={valid_to_prima}")
            prima_api.setPrimaDates(user.prima_id, valid_from_prima, valid_to_prima)

        self.stdout.write("End fill valid_from and valid_to on users.")
