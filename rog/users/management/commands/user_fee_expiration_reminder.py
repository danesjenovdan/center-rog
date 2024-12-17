from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from home.email_utils import send_email
from payments.models import Payment, PaymentItemType, PaymentPlanEvent


class Command(BaseCommand):
    help = "Reminder for user fee expiration."

    def handle(self, *args, **options):
        self.stdout.write("Start sending notifications for user fee expiration.")

        payment_plans_1 = PaymentPlanEvent.objects.filter(
            valid_to__range=(
                datetime.now().date() - timedelta(days=0),
                datetime.now() + timedelta(days=1),
            ),
            payment_item_type=PaymentItemType.UPORABNINA,
            payment__status=Payment.Status.SUCCESS,
        ).exclude(notification_1_sent=True)

        for payment_plan in payment_plans_1:
            if not payment_plan.payment.user:
                continue

            # Skip if user has another uporabnina payment plan after this one
            if (
                PaymentPlanEvent.objects.filter(
                    payment__user=payment_plan.payment.user,
                    payment_item_type=PaymentItemType.UPORABNINA,
                    payment__status=Payment.Status.SUCCESS,
                ).last()
                != payment_plan
            ):
                continue

            send_email(
                payment_plan.payment.user.email,
                "emails/user_fee_expired.html",
                "Center Rog – obvestilo o poteku uporabnine // your user package has expired",
                {
                    "payment_plan": payment_plan,
                },
            )
            self.stdout.write(
                f"Email (user fee) sent for user id: {payment_plan.payment.user.id} before expiration of payment plan: {payment_plan.id}"
            )

            payment_plan.notification_1_sent = True
            payment_plan.save()

        payment_plans_7 = (
            PaymentPlanEvent.objects.filter(
                valid_to__range=(
                    datetime.now().date() + timedelta(days=7),
                    datetime.now(),
                ),
                payment_item_type=PaymentItemType.UPORABNINA,
                payment__status=Payment.Status.SUCCESS,
            )
            .exclude(notification_7_sent=True)
            .exclude(notification_1_sent=True)
        )

        for payment_plan in payment_plans_7:
            if not payment_plan.payment.user:
                continue

            # Skip if user has another uporabnina payment plan after this one
            if (
                PaymentPlanEvent.objects.filter(
                    payment__user=payment_plan.payment.user,
                    payment_item_type=PaymentItemType.UPORABNINA,
                    payment__status=Payment.Status.SUCCESS,
                ).last()
                != payment_plan
            ):
                continue

            send_email(
                payment_plan.payment.user.email,
                "emails/user_fee_expiration_reminder_7.html",
                "Center Rog - čez en teden poteče tvoj uporabniški paket // in 1 Week your user package will expire",
                {
                    "payment_plan": payment_plan,
                    "name": payment_plan.payment.user.first_name,
                },
            )

            payment_plan.notification_7_sent = True
            payment_plan.save()
            self.stdout.write(
                f"Email (user fee) sent for user id: {payment_plan.payment.user.id} 7 days before expiration of payment plan: {payment_plan.id}"
            )

        payment_plans_30 = (
            PaymentPlanEvent.objects.filter(
                valid_to__range=(
                    datetime.now().date() + timedelta(days=30),
                    datetime.now(),
                ),
                payment_item_type=PaymentItemType.UPORABNINA,
                payment__status=Payment.Status.SUCCESS,
            )
            .exclude(notification_30_sent=True)
            .exclude(notification_7_sent=True)
            .exclude(notification_1_sent=True)
        )

        for payment_plan in payment_plans_30:
            if not payment_plan.payment.user:
                continue

            # Skip if user has another uporabnina payment plan after this one
            if (
                PaymentPlanEvent.objects.filter(
                    payment__user=payment_plan.payment.user,
                    payment_item_type=PaymentItemType.UPORABNINA,
                    payment__status=Payment.Status.SUCCESS,
                ).last()
                != payment_plan
            ):
                continue

            send_email(
                payment_plan.payment.user.email,
                "emails/user_fee_expiration_reminder_30.html",
                "Center Rog - čez en mesec poteče tvoj uporabniški paket // in 1 Month your user package will expire",
                {
                    "payment_plan": payment_plan,
                    "name": payment_plan.payment.user.first_name,
                },
            )

            payment_plan.notification_30_sent = True
            payment_plan.save()
            self.stdout.write(
                f"Email (user fee) sent for user id: {payment_plan.payment.user.id} 30 days before expiration of payment plan: {payment_plan.id}"
            )

        self.stdout.write("End sending notifications for membership expiration.")
