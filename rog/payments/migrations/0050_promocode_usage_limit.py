# Generated by Django 4.1.11 on 2024-03-20 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0049_alter_paymentplanevent_payment_item_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='usage_limit',
            field=models.IntegerField(default=0),
        ),
    ]
