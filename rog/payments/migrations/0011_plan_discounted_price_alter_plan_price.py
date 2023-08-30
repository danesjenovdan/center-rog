# Generated by Django 4.1.10 on 2023-08-30 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_alter_plan_pantheon_ident_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='discounted_price',
            field=models.IntegerField(default=10, help_text='Price for younger than 26 years old and older than 65', verbose_name='Discounted price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plan',
            name='price',
            field=models.IntegerField(verbose_name='Price'),
        ),
    ]
