# Generated by Django 4.1.9 on 2023-06-30 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_plan_options'),
        ('users', '0013_alter_user_legal_person_address_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membershiptype',
            name='price',
        ),
        migrations.AddField(
            model_name='membershiptype',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.plan', verbose_name='Plačilni paket'),
        ),
    ]
