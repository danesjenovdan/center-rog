# Generated by Django 4.1.10 on 2023-09-05 10:38

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0018_remove_newspage_archived_delete_newslistarchivepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='gallery',
            field=wagtail.fields.StreamField([('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Slika')), ('image_description', wagtail.blocks.TextBlock(label='Podnapis k sliki', required=False))]))], blank=True, null=True, use_json_field=True, verbose_name='Galerija'),
        ),
    ]
