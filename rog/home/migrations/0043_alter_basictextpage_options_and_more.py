# Generated by Django 4.1.9 on 2023-07-01 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_remove_contentpage_color_scheme_contentpage_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basictextpage',
            options={'verbose_name': 'Osnovna stran z besedilom', 'verbose_name_plural': 'Osnovne strani z besedilom'},
        ),
        migrations.AlterModelOptions(
            name='contentpage',
            options={'verbose_name': 'Osnovna stran z moduli', 'verbose_name_plural': 'Osnovne strani z moduli'},
        ),
    ]