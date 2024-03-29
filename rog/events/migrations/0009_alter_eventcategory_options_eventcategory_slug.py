# Generated by Django 4.1.9 on 2023-06-27 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_eventcategory_options_eventpage_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'verbose_name': 'Kategorija dogodkov', 'verbose_name_plural': 'Kategorije dogodkov'},
        ),
        migrations.AddField(
            model_name='eventcategory',
            name='slug',
            field=models.SlugField(default='example'),
            preserve_default=False,
        ),
    ]
