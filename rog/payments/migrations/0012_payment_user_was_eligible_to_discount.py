# Generated by Django 4.1.10 on 2023-08-30 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_plan_discounted_price_alter_plan_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user_was_eligible_to_discount',
            field=models.BooleanField(default=False),
        ),
    ]
