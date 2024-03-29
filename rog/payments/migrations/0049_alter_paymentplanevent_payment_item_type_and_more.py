# Generated by Django 4.1.11 on 2024-03-20 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0048_plan_extend_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentplanevent',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Clanarina'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek'), ('training', 'Usposabljanje')], default='clanarina', max_length=20),
        ),
        migrations.AlterField(
            model_name='plan',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Clanarina'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek'), ('training', 'Usposabljanje')], default='clanarina', max_length=20),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Clanarina'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek'), ('training', 'Usposabljanje')], default='clanarina', max_length=20),
        ),
    ]
