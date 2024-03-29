# Generated by Django 4.1.10 on 2023-08-10 08:27

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0060_rename_footer_images_metasettings_footer_logos'),
    ]

    operations = [
        migrations.AddField(
            model_name='metasettings',
            name='footer_random_images',
            field=wagtail.fields.StreamField([('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())], label='Slika'))], blank=True, use_json_field=True, verbose_name='Naključne slike v nogi'),
        ),
    ]
