# Generated by Django 4.1.11 on 2023-09-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0022_remove_payment_promo_code_paymentplan_promo_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='description_item_1',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Postavka 1'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='description_item_2',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Postavka 2'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='description_item_3',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Postavka 3'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='description_item_4',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Postavka 4'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='description_item_5',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Postavka 5'),
        ),
    ]
