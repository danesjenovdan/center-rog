# Generated by Django 4.1.10 on 2023-08-31 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_alter_eventcategory_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='notice',
            field=models.CharField(blank=True, max_length=45, verbose_name='Opomba'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='tag',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Oznaka na kartici'),
        ),
    ]