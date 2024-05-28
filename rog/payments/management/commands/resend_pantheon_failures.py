from users.models import User
from events.models import EventCategory
from payments.models import Payment, Plan

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Setup testing data"

    def filter_letters(self, input):
        return "".join(filter(str.isalpha, input))

    def handle(self, *args, **options):
        # set name to users without name
        users_without_name = User.objects.filter(first_name="", last_name="")
        for user in users_without_name:
            user.first_name = self.filter_letters(
                " ".join(user.email.split("@")[0].split("."))
            )
            print(user.first_name)
            user.save()

        # Resend users
        for user in User.objects.filter(saved_in_pantheon=False):
            user.save()

        # resend event categories
        for event in EventCategory.objects.filter(saved_in_pantheon=False):
            event.save()

        # resend plans
        for plan in Plan.objects.filter(saved_in_pantheon=False):
            plan.save()

        # resend payments
        for payment in Payment.objects.filter(
            saved_in_pantheon=False,
            amount__gt=0,
            successed_at__year__gte=2024,
            successed_at__isnull=False,
            transaction_success_at__isnull=False,
        ).order_by("invoice_number"):
            payment.save_to_pantheon()
