# Generated by Django 4.1.11 on 2024-01-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0044_auto_20240116_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='items',
            field=models.ManyToManyField(blank=True, help_text='Items in payment', related_name='payments', through='payments.PaymentPlanEvent', to='payments.plan'),
        ),
    ]
