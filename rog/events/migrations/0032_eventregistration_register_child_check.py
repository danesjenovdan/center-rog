# Generated by Django 4.1.11 on 2023-12-19 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0031_eventpage_pantheon_ident"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventregistration",
            name="register_child_check",
            field=models.BooleanField(
                default=False, verbose_name="Na dogodek prijavljam otroka"
            ),
        ),
    ]
