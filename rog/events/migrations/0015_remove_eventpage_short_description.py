# Generated by Django 4.1.10 on 2023-08-08 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_alter_eventpage_end_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='short_description',
        ),
    ]