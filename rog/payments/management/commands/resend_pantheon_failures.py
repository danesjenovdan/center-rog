from users.models import User
from events.models import EventPage
from payments.models import Payment, Plan

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Setup testing data"

    def handle(self, *args, **options):
        for user in User.objects.filter(saved_in_pantheon=False):
            user.save()

        for event in EventPage.objects.filter(saved_in_pantheon=False):
            event.save()

        for plan in Plan.objects.filter(saved_in_pantheon=False):
            plan.save()

        for payment in Payment.objects.filter(saved_in_pantheon=False):
            payment.save()
