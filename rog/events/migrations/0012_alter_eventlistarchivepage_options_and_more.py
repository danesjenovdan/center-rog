# Generated by Django 4.1.9 on 2023-07-03 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0011_alter_eventpage_options_eventpage_archived_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventlistarchivepage",
            options={
                "verbose_name": "Arhiv dogodkov",
                "verbose_name_plural": "Arhivi dogodkov",
            },
        ),
        migrations.AlterModelOptions(
            name="eventlistpage",
            options={
                "verbose_name": "Seznam dogodkov",
                "verbose_name_plural": "Seznami dogodkov",
            },
        ),
    ]
