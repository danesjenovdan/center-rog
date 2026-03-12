from users.prima_api import PrimaApi
from users.models import User
from home.models import Workshop
from django.core.management.base import BaseCommand

prima_api = PrimaApi()


class Command(BaseCommand):
    help = "Update workshops from Prima API"

    def handle(self, *args, **options):
        self.stdout.write("Start updating workshops from Prima API")

        users = User.objects.filter(prima_id__isnull=False)
        for user in users:
            data, message = prima_api.readUserGroups(user.prima_id)
            if message == "Success":
                data_list = data["UsersList"]
                if isinstance(data_list, dict):
                    data_list = [data_list]  # Convert to list if it's a single dict
                for group in data_list:
                    group_id = group["@LstID"]
                    if group_id in ["100", "101", "102"]:
                        # skip memberships and subscriptions
                        continue
                    else:
                        print(f"User {user.email} is in group {group_id}")
                        user.workshops_attended.add(
                            Workshop.objects.get(prima_id=group_id)
                        )
               

