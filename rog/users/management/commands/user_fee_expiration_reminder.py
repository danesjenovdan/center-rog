from django.core.management.base import BaseCommand

from datetime import datetime, timedelta

from payments.models import PaymentPlanEvent
from home.email_utils import send_email

class Command(BaseCommand):
    help = 'Reminder for membership expiration.'

    def handle(self, *args, **options):
        self.stdout.write("Start sending notifications for user fee expiration.")

        payment_plans_1 = PaymentPlanEvent.objects.filter(
            valid_to__range=(datetime.now().date() - timedelta(days=0), datetime.now() + timedelta(days=1))
        ).exclude(notification_1_sent=True)

        for payment_plan in payment_plans_1:
            if not payment_plan.payment.user:
                continue

            send_email(
                payment_plan.payment.user.email,
                "emails/user_fee_expired.html",
                'Center Rog – obvestilo o poteku uporabnine',
                {
                    "payment_plan": payment_plan,
                },
            )

            payment_plan.notification_1_sent = True
            payment_plan.save()


        payment_plans_7 = PaymentPlanEvent.objects.filter(
            valid_to__range=(datetime.now().date() - timedelta(days=7), datetime.now())
        ).exclude(
            notification_7_sent=True
        ).exclude(
            notification_1_sent=True
        )

        for payment_plan in payment_plans_7:
            if not payment_plan.payment.user:
                continue

            send_email(
                payment_plan.payment.user.email,
                "emails/user_fee_expiration_reminder.html",
                'Center Rog - obvestilo o skorajšnjem poteku paketa – še en teden',
                {
                    "how_many": "en teden",
                    "payment_plan": payment_plan,
                },
            )

            payment_plan.notification_7_sent = True
            payment_plan.save()


        payment_plans_30 = PaymentPlanEvent.objects.filter(
            valid_to__range=(datetime.now().date() - timedelta(days=30), datetime.now())
        ).exclude(
            notification_30_sent=True
        ).exclude(
            notification_7_sent=True
        ).exclude(
            notification_1_sent=True
        )

        for payment_plan in payment_plans_30:
            if not payment_plan.payment.user:
                continue

            send_email(
                payment_plan.payment.user.email,
                "emails/user_fee_expiration_reminder.html",
                'Center Rog - obvestilo o skorajšnjem poteku paketa – še en mesec',
                {
                    "how_many": "en mesec",
                    "payment_plan": payment_plan,
                },
            )

            payment_plan.notification_30_sent = True
            payment_plan.save()

        self.stdout.write("End sending notifications for membership expiration.")

