# Generated by Django 4.1.10 on 2023-08-17 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0065_lablistpage_intro_text_en_lablistpage_intro_text_sl_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentpage',
            name='body_en',
        ),
        migrations.RemoveField(
            model_name='contentpage',
            name='body_sl',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body_sl',
        ),
        migrations.RemoveField(
            model_name='lablistpage',
            name='intro_text_en',
        ),
        migrations.RemoveField(
            model_name='lablistpage',
            name='intro_text_sl',
        ),
        migrations.RemoveField(
            model_name='marketstorelistpage',
            name='intro_text_en',
        ),
        migrations.RemoveField(
            model_name='marketstorelistpage',
            name='intro_text_sl',
        ),
        migrations.RemoveField(
            model_name='residencelistpage',
            name='intro_text_en',
        ),
        migrations.RemoveField(
            model_name='residencelistpage',
            name='intro_text_sl',
        ),
        migrations.RemoveField(
            model_name='studiolistpage',
            name='intro_text_en',
        ),
        migrations.RemoveField(
            model_name='studiolistpage',
            name='intro_text_sl',
        ),
    ]
