# Generated by Django 4.1.11 on 2023-09-13 12:54

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0026_alter_user_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("F", "ženski"), ("M", "moški"), ("O", "drugo")],
                default="O",
                max_length=1,
                verbose_name="Spol",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender_other",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="Spol (drugo)"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="birth_date",
            field=models.DateField(
                default=datetime.datetime(1970, 1, 1, 0, 0),
                verbose_name="Datum rojstva",
            ),
            preserve_default=False,
        ),
    ]
