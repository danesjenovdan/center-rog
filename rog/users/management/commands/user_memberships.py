from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = "For users with memberships expiring in 2024, set membership.valid_to to 1.1.2025."

    def handle(self, *args, **options):
        self.stdout.write("Start updating user memberships expiration dates")

        new_valid_to = timezone.now().replace(
            year=2025, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )

        for user in User.objects.all():
            membership = user.membership

            if membership:
                if membership.type.plan and membership.valid_to < new_valid_to:
                    self.stdout.write(f"For user: {user.email}")
                    self.stdout.write(f"    update membership: {membership}")
                    self.stdout.write(
                        f"    valid_to: {membership.valid_to} -> {new_valid_to}"
                    )
                    membership.valid_to = new_valid_to
                    membership.save()

        self.stdout.write("Finished!")
