# Generated by Django 4.1.9 on 2023-07-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_labpage_lab_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='prima_group_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Prima group id'),
        ),
        migrations.AddField(
            model_name='tool',
            name='prima_location_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Prima location id'),
        ),
    ]
