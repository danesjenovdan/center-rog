# Generated by Django 4.1.11 on 2024-03-21 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0047_alter_paymentplanevent_event_registration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='name_en',
            field=models.CharField(help_text='Npr. letna uporabnina', max_length=100, null=True, verbose_name='Ime paketa'),
        ),
        migrations.AddField(
            model_name='plan',
            name='name_sl',
            field=models.CharField(help_text='Npr. letna uporabnina', max_length=100, null=True, verbose_name='Ime paketa'),
        ),
    ]
