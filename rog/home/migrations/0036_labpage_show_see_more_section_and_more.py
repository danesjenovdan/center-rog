# Generated by Django 4.1.9 on 2023-06-28 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_labpage_image_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='labpage',
            name='show_see_more_section',
            field=models.BooleanField(default=False, verbose_name='Pokaži več'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='show_see_more_section',
            field=models.BooleanField(default=False, verbose_name='Pokaži več'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='show_see_more_section',
            field=models.BooleanField(default=False, verbose_name='Pokaži več'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='show_see_more_section',
            field=models.BooleanField(default=False, verbose_name='Pokaži več'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='show_see_more_section',
            field=models.BooleanField(default=False, verbose_name='Pokaži več'),
        ),
    ]