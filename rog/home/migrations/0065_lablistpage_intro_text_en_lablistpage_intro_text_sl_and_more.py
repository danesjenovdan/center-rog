# Generated by Django 4.1.10 on 2023-08-17 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0064_studiolistpage_intro_text_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lablistpage",
            name="intro_text_en",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="lablistpage",
            name="intro_text_sl",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="marketstorelistpage",
            name="intro_text_en",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="marketstorelistpage",
            name="intro_text_sl",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="residencelistpage",
            name="intro_text_en",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="residencelistpage",
            name="intro_text_sl",
            field=models.TextField(blank=True, null=True),
        ),
    ]
