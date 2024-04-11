# Generated by Django 4.1.11 on 2024-03-26 15:54

from django.db import migrations, models
import payments.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0052_merge_20240321_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='code',
            field=models.CharField(default=payments.models.generate_promo_code, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='number_of_uses',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='usage_limit',
            field=models.IntegerField(default=0, help_text='How many times can the code be used? 0 means unlimited.'),
        ),
    ]