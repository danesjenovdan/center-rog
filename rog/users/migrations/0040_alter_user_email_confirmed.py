# Generated by Django 4.1.11 on 2024-06-20 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0039_auto_20240528_1727"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email_confirmed",
            field=models.BooleanField(
                default=False, verbose_name="e-pošta je potrjena?"
            ),
        ),
    ]
