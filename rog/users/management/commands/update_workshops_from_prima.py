from users.prima_api import PrimaApi
from home.models import Workshop
from django.core.management.base import BaseCommand

prima_api = PrimaApi()


class Command(BaseCommand):
    help = "Update workshops from Prima API"

    def handle(self, *args, **options):
        self.stdout.write("Start updating workshops from Prima API")

        prima_groups, status = prima_api.getPrimaGroups()
        if status == "Success":
            for group in prima_groups["List"]:
                group_id = group["@LstID"]
                group_name = group["@LstName"]
                if group_id in ["100", "101", "102"]:  # Samo za skupine članarine in uporabnine
                    # skip memberships and subscriptions
                    continue
                else:
                    Workshop.objects.update_or_create(
                        prima_id=group_id,
                        defaults={"name": group_name},
                    )

