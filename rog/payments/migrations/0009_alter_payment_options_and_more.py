# Generated by Django 4.1.10 on 2023-08-17 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_payment_saved_in_pantheon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Naročil0', 'verbose_name_plural': 'Naročila'},
        ),
        migrations.AlterField(
            model_name='payment',
            name='saved_in_pantheon',
            field=models.BooleanField(default=False, help_text='Ali račun že shranjen v Pantheon ali preprečite shranjevanje računa v Pantheon'),
        ),
    ]