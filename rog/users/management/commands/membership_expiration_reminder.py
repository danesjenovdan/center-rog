from django.core.management.base import BaseCommand

from datetime import datetime, timedelta

from users.models import Membership
from home.email_utils import send_email

class Command(BaseCommand):
    help = 'Reminder for membership expiration.'

    def handle(self, *args, **options):
        self.stdout.write("Start sending notifications for membership expiration.")

        memberships_1 = Membership.objects.filter(
            active=True,
            valid_to__range=(datetime.now().date() - timedelta(days=1), datetime.now())
        ).exclude(notification_1_sent=True)

        for membership in memberships_1:
            if not membership.user:
                continue

            self.send('1 dan', membership)

            membership.notification_1_sent = True
            membership.save()


        memberships_7 = Membership.objects.filter(
            active=True,
            valid_to__range=(datetime.now().date() - timedelta(days=7), datetime.now())
        ).exclude(
            notification_7_sent=True
        ).exclude(
            notification_1_sent=True
        )

        for membership in memberships_7:
            if not membership.user:
                continue

            self.send('7 dni', membership)

            membership.notification_7_sent = True
            membership.save()


        memberships_14 = Membership.objects.filter(
            active=True,
            valid_to__range=(datetime.now().date() - timedelta(days=14), datetime.now())
        ).exclude(
            notification_14_sent=True
        ).exclude(
            notification_7_sent=True
        ).exclude(
            notification_1_sent=True
        )

        for membership in memberships_14:
            if not membership.user:
                continue

            self.send('14 dni', membership)

            membership.notification_14_sent = True
            membership.save()


        memberships_30 = Membership.objects.filter(
            active=True,
            valid_to__range=(datetime.now().date() - timedelta(days=30), datetime.now())
        ).exclude(
            notification_30_sent=True
        ).exclude(
            notification_14_sent=True
        ).exclude(
            notification_7_sent=True
        ).exclude(
            notification_1_sent=True
        )

        for membership in memberships_30:
            if not membership.user:
                continue

            self.send('30 dni', membership)

            membership.notification_30_sent = True
            membership.save()

        self.stdout.write("End sending notifications for membership expiration.")

    def send(self, days, membership):
        send_email(
                membership.user.email,
                "emails/membership_expiration_reminder.html",
                f"Članarina poteče čez manj kot {days}",
                {
                    "membership": membership,
                }
            )
        membership.notification_1_sent = True
        membership.save()
