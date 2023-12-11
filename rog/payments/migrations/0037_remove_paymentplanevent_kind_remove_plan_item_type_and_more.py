# Generated by Django 4.1.11 on 2023-12-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0036_auto_20231206_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentplanevent',
            name='kind',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='item_type',
        ),
        migrations.RemoveField(
            model_name='promocode',
            name='item_type',
        ),
        migrations.AddField(
            model_name='paymentplanevent',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Clanarina'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek')], default='clanarina', max_length=20),
        ),
        migrations.AlterField(
            model_name='plan',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Clanarina'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek')], default='clanarina', max_length=20),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Clanarina'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek')], default='clanarina', max_length=20),
        ),
    ]
