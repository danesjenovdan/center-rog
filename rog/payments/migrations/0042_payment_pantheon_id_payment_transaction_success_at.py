# Generated by Django 4.1.11 on 2024-01-15 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0041_auto_20231207_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='pantheon_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_success_at',
            field=models.DateTimeField(blank=True, help_text='When payment transaction was provided', null=True),
        ),
    ]