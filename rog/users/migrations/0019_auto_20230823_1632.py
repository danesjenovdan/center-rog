# Generated by Django 4.1.10 on 2023-08-23 14:32

from django.db import migrations

def migrate_memberships(apps, schema_editor):
    User = apps.get_model("users", "User")

    users = User.objects.all()
    for user in users:
        if user.membership:
            membership = user.membership
            membership.user = user
            membership.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_membership_notification_14_sent_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_memberships),
    ]
