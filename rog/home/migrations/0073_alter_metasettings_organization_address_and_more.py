# Generated by Django 4.1.10 on 2023-08-28 09:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0072_tool_more_information_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metasettings',
            name='organization_address',
            field=models.TextField(blank=True, null=True, verbose_name='Ulica in hišna številka'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='organization_country',
            field=models.TextField(blank=True, null=True, verbose_name='Država'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='organization_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-pošta'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='organization_name',
            field=models.TextField(blank=True, null=True, verbose_name='Ime'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='organization_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefonska številka'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='organization_post',
            field=models.TextField(blank=True, null=True, verbose_name='Pošta'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='organization_postal_number',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)], verbose_name='Poštna številka'),
        ),
    ]
