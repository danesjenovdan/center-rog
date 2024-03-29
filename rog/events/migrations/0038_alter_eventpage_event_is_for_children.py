# Generated by Django 4.1.11 on 2024-02-07 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0037_eventpage_event_is_for_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='event_is_for_children',
            field=models.BooleanField(default=False, help_text='Prijava na dogodek zahteva vpis vsaj enega otroka', verbose_name='Dogodek je za otroke'),
        ),
    ]
