# Generated by Django 4.1.9 on 2023-07-03 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0009_alter_newspage_options_newspage_archived_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newslistarchivepage",
            options={
                "verbose_name": "Arhiv novic",
                "verbose_name_plural": "Arhivi novic",
            },
        ),
        migrations.AlterModelOptions(
            name="newslistpage",
            options={
                "verbose_name": "Seznam novic",
                "verbose_name_plural": "Seznami novic",
            },
        ),
        migrations.AlterModelOptions(
            name="newspage",
            options={"verbose_name": "Novica", "verbose_name_plural": "Novice"},
        ),
    ]
