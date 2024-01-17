# Generated by Django 4.1.11 on 2024-01-15 12:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0033_eventcategory_name_en_eventcategory_name_sl'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
