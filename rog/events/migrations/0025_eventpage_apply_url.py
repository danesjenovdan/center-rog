# Generated by Django 4.1.11 on 2023-10-18 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_eventlistarchivepage_meta_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='apply_url',
            field=models.URLField(blank=True, verbose_name='Povezava za prijavo (če je prazno, se gumb skrije)'),
        ),
    ]
