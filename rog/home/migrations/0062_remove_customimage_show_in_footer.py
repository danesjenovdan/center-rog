# Generated by Django 4.1.10 on 2023-08-10 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0061_metasettings_footer_random_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customimage',
            name='show_in_footer',
        ),
    ]
