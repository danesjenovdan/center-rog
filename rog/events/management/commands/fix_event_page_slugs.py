from django.core.management.base import BaseCommand, CommandError
from events.models import EventPage


class Command(BaseCommand):
    help = "Fixes slugs for event pages"

    def handle(self, *args, **options):
        count = EventPage.objects.count()
        self.stdout.write(f"Fixing slugs for {count} event pages...")

        i = 0
        for event in EventPage.objects.all():
            i += 1
            print(f"Processing {i}/{count} (ID: {event.id})...", end="\r")
            should_save = False
            if event.slug:
                if not event.slug_en:
                    event.slug_en = event.slug
                    should_save = True
                if not event.slug_sl:
                    event.slug_sl = event.slug
                    should_save = True
            if should_save:
                event.save()

        self.stdout.write("\n")
        self.stdout.write(self.style.SUCCESS("Done!"))
