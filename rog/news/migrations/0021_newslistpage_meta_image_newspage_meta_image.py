# Generated by Django 4.1.11 on 2023-10-13 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0100_basictextpage_meta_image_contentpage_meta_image_and_more'),
        ('news', '0020_alter_newspage_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslistpage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.customimage', verbose_name='Meta slika'),
        ),
        migrations.AddField(
            model_name='newspage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.customimage', verbose_name='Meta slika'),
        ),
    ]
