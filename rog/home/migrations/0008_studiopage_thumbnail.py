# Generated by Django 4.1.9 on 2023-05-23 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('home', '0007_labpage_thumbnail_labpage_thumbnail_animation'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiopage',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
