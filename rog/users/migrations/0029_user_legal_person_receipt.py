# Generated by Django 4.1.11 on 2023-09-13 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_user_legal_person_vat'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='legal_person_receipt',
            field=models.BooleanField(default=False, verbose_name='Račun za pravno osebo'),
        ),
    ]
