# Generated by Django 4.1.11 on 2024-01-17 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_eventregistration_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='saved_in_pantheon',
            field=models.BooleanField(default=False, help_text='Ali račun že shranjen v Pantheon ali preprečite shranjevanje računa v Pantheon'),
        ),
    ]
