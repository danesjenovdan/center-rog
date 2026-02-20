from users.models import Membership, User
from django.utils import timezone

from users.prima_api import PrimaApi


def set_names_to_prima_users():
    prima_api = PrimaApi()
    users = User.objects.filter(prima_id__isnull=False).exclude(
        first_name="", last_name=""
    )
    for user in users:
        data, msg = prima_api.readUsers(user_id=user.prima_id)
        if not "user" in data.keys():
            continue
        if not "@UsrName" in data["user"].keys():
            prima_api.updateUserName(
                user_id=user.prima_id,
                name=user.first_name,
                last_name=user.last_name,
            )


def export_active_members_to_csv():
    active_memberships = Membership.objects.filter(
        valid_to__gte=timezone.now(),
        active=True,
    )

    with open("members.csv", "w") as f:
        for active_membership in active_memberships:
            user = active_membership.user
            f.write(f"{user.first_name},{user.last_name},{user.email}\n")


def count_prima_users_without_names():
    prima_api = PrimaApi()
    i=0
    users = User.objects.filter(prima_id__isnull=False).exclude(
        first_name="", last_name=""
    )
    for user in users:
        data, msg = prima_api.readUsers(user_id=user.prima_id)
        if not "user" in data.keys():
            continue
        if not '@UsrName' in data["user"].keys():
            i+=1
            continue
        if not (data["user"]["@UsrName"] or data["user"]["@UsrName"]):
            i+=1

    print(users.count(), i)

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}.{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}.{i}", item))
        else:
            items.append((new_key, v))
    return dict(items)
