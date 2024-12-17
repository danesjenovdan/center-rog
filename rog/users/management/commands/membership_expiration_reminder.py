from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from home.email_utils import send_email
from users.models import Membership


class Command(BaseCommand):
    help = "Reminder for membership expiration."

    def handle(self, *args, **options):
        self.stdout.write("Start sending notifications for membership expiration.")

        memberships_1 = Membership.objects.filter(
            active=True,
            valid_to__range=(
                datetime.now().date() - timedelta(days=0),
                datetime.now() + timedelta(days=1),
            ),
        ).exclude(notification_1_sent=True)

        for membership in memberships_1:
            if not membership.user:
                continue

            if (
                membership.user.get_last_active_membership().valid_to
                > membership.valid_to
            ):
                continue

            send_email(
                membership.user.email,
                "emails/membership_expired.html",
                "Center Rog – obvestilo o poteku članstva // your membership has expired",
                {
                    "membership": membership,
                },
            )

            membership.notification_1_sent = True
            membership.save()
            self.stdout.write(
                f"Email (membership) sent for user id: {membership.user.id} before expiration of membership: {membership.id} {membership.valid_to}"
            )

        memberships_7 = (
            Membership.objects.filter(
                active=True,
                valid_to__range=(
                    datetime.now().date() + timedelta(days=7),
                    datetime.now(),
                ),
            )
            .exclude(notification_7_sent=True)
            .exclude(notification_1_sent=True)
        )

        for membership in memberships_7:
            if not membership.user:
                continue

            if (
                membership.user.get_last_active_membership().valid_to
                > membership.valid_to
            ):
                continue

            send_email(
                membership.user.email,
                "emails/membership_expiration_reminder.html",
                "Center Rog – čez en teden se izteče tvoje članstvo // in 1 Week your membership will expire",
                {
                    "membership": membership,
                    "name": membership.user.first_name,
                },
            )

            membership.notification_7_sent = True
            membership.save()
            self.stdout.write(
                f"Email (membership) sent for user id: {membership.user.id} 7 days before expiration of membership: {membership.id} {membership.valid_to}"
            )

        memberships_30 = (
            Membership.objects.filter(
                active=True,
                valid_to__range=(
                    datetime.now().date() + timedelta(days=30),
                    datetime.now(),
                ),
            )
            .exclude(notification_30_sent=True)
            .exclude(notification_7_sent=True)
            .exclude(notification_1_sent=True)
        )

        for membership in memberships_30:
            if not membership.user:
                continue

            if (
                membership.user.get_last_active_membership().valid_to
                > membership.valid_to
            ):
                continue

            send_email(
                membership.user.email,
                "emails/membership_expiration_reminder_30.html",
                "Center Rog – čez en mesec se izteče tvoje članstvo // in 1 Month your membership will expire",
                {"membership": membership, "name": membership.user.first_name},
            )

            membership.notification_30_sent = True
            membership.save()
            self.stdout.write(
                f"Email (membership) sent for user id: {membership.user.id} 30 days before expiration of membership: {membership.id} {membership.valid_to}"
            )

        self.stdout.write("End sending notifications for membership expiration.")
