# Generated by Django 4.1.10 on 2023-08-08 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_remove_eventpage_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='location',
            field=models.TextField(blank=True, default='Center Rog', verbose_name='Lokacija'),
        ),
    ]
