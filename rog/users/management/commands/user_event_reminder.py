from django.core.management.base import BaseCommand

from datetime import datetime, timedelta

from payments.models import PaymentPlanEvent
from events.models import EventPage
from home.email_utils import send_email

class Command(BaseCommand):
    help = 'Reminder for membership expiration.'

    def handle(self, *args, **options):
        self.stdout.write("Start sending notifications for user fee expiration.")
        events = EventPage.objects.filter(
            start_day__range=(datetime.now().date(), (datetime.now() + timedelta(days=2)).date())
        )
        for event in events:
            for event_registration in event.event_registrations.all():
                if event_registration.user:
                    payment_plan_event = PaymentPlanEvent.objects.filter(event_registration=event_registration).first()
                    if payment_plan_event and not payment_plan_event.notification_1_sent:
                        send_email(
                            event_registration.user.email,
                            'emails/user_event_reminder.html',
                            f'Center Rog – obvestilo prihajajočem dogodku: {event.title}',
                            {
                                "event": event,
                            },
                        )
                        payment_plan_event.notification_1_sent=True
                        payment_plan_event.save()

        self.stdout.write("End sending notifications for event.")

