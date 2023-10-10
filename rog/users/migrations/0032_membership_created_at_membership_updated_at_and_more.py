# Generated by Django 4.1.11 on 2023-10-10 09:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_remove_membership_notification_14_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membership',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
