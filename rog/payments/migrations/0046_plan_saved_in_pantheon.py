# Generated by Django 4.1.11 on 2024-01-18 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0045_alter_payment_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='saved_in_pantheon',
            field=models.BooleanField(default=False, help_text='Ali račun že shranjen v Pantheon ali preprečite shranjevanje računa v Pantheon'),
        ),
    ]
