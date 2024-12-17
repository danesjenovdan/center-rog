# Generated by Django 4.1.11 on 2024-05-28 15:27

from django.db import migrations


def confirm_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.all().update(email_confirmed=True)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0038_user_email_confirmed_confirmemail"),
    ]

    operations = [migrations.RunPython(confirm_users)]
