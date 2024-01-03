from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.prima_api import PrimaApi

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

            last_active_membership = user.get_last_active_membership()
            if last_active_membership:
                valid_from = last_active_membership.valid_from
                valid_to = last_active_membership.valid_to

            valid_from_prima = valid_from.strftime("%Y-%m-%d %H:%M:%S")
            valid_to_prima = valid_to.strftime("%Y-%m-%d %H:%M:%S")

            self.stdout.write(f"{user.email} - prima_id={user.prima_id}")
            self.stdout.write(f"  valid_from={valid_from_prima}")
            self.stdout.write(f"    valid_to={valid_to_prima}")
            prima_api.setUporabninaDates(user.prima_id, valid_from_prima, valid_to_prima)

        self.stdout.write("End fill valid_from and valid_to on users.")
