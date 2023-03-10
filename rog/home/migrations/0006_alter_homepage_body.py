# Generated by Django 4.1.7 on 2023-03-01 09:49

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StreamBlock([('color_section', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('white', 'Bela'), ('yellow', 'Rumena'), ('purple', 'Vijolična'), ('gradient_green_yellow', 'Zeleno-rumena'), ('gradient_purple_green', 'Vijolično-zelena')], label='Barva')), ('body', wagtail.blocks.StreamBlock([], required=False))]))]))], default='', use_json_field=False, verbose_name='Barvna sekcija'),
        ),
    ]
