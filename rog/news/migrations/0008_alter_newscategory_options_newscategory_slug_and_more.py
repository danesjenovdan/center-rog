# Generated by Django 4.1.9 on 2023-06-27 12:44

import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0007_alter_newspage_hero_image_alter_newspage_thumbnail"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newscategory",
            options={
                "verbose_name": "Kategorija novic",
                "verbose_name_plural": "Kategorije novic",
            },
        ),
        migrations.AddField(
            model_name="newscategory",
            name="slug",
            field=models.SlugField(default="example"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="newspage",
            name="gallery",
            field=wagtail.fields.StreamField(
                [("image", wagtail.images.blocks.ImageChooserBlock())],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
