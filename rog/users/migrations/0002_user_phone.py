# Generated by Django 4.1.7 on 2023-03-24 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
