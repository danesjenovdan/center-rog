from users.models import User
from events.models import EventCategory
from payments.models import Payment, Plan

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Setup testing data"

    def handle(self, *args, **options):
        for user in User.objects.filter(saved_in_pantheon=False).exclude(first_name=""):
            user.save()

        for event in EventCategory.objects.filter(saved_in_pantheon=False):
            event.save()

        for plan in Plan.objects.filter(saved_in_pantheon=False):
            plan.save()

        for payment in Payment.objects.filter(saved_in_pantheon=False, amount__gt=0, successed_at__year__gte=2024, successed_at__isnull=False):
            payment.save()
