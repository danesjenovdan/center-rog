# Generated by Django 4.1.11 on 2023-09-19 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0024_alter_payment_amount_alter_plan_discounted_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentplan',
            name='plan_name',
            field=models.CharField(default='tmp', help_text='Npr. letna uporabnina', max_length=100, verbose_name='Ime paketa na dan nakupa'),
            preserve_default=False,
        ),
    ]
