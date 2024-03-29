# Generated by Django 4.1.10 on 2023-09-08 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0021_plan_description_plan_description_item_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='promo_code',
        ),
        migrations.AddField(
            model_name='paymentplan',
            name='promo_code',
            field=models.ForeignKey(blank=True, help_text='The promo code used for this payment plan', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_plans', to='payments.promocode'),
        ),
    ]
