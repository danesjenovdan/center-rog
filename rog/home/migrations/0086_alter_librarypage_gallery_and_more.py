# Generated by Django 4.1.10 on 2023-09-01 10:28

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0085_alter_labpage_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarypage',
            name='gallery',
            field=wagtail.fields.StreamField([('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Slika')), ('image_description', wagtail.blocks.TextBlock(label='Podnapis k sliki'))]))], blank=True, null=True, use_json_field=True, verbose_name='Galerija'),
        ),
        migrations.AlterField(
            model_name='marketstorepage',
            name='gallery',
            field=wagtail.fields.StreamField([('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Slika')), ('image_description', wagtail.blocks.TextBlock(label='Podnapis k sliki'))]))], blank=True, null=True, use_json_field=True, verbose_name='Galerija'),
        ),
        migrations.AlterField(
            model_name='residencepage',
            name='gallery',
            field=wagtail.fields.StreamField([('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Slika')), ('image_description', wagtail.blocks.TextBlock(label='Podnapis k sliki'))]))], blank=True, null=True, use_json_field=True, verbose_name='Galerija'),
        ),
        migrations.AlterField(
            model_name='studiopage',
            name='gallery',
            field=wagtail.fields.StreamField([('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Slika')), ('image_description', wagtail.blocks.TextBlock(label='Podnapis k sliki'))]))], blank=True, null=True, use_json_field=True, verbose_name='Galerija'),
        ),
    ]
