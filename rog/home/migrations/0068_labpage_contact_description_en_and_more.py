# Generated by Django 4.1.10 on 2023-08-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0067_contentpage_body_en_contentpage_body_sl_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='labpage',
            name='contact_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='contact_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='image_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='image_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='contact_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='contact_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='image_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='image_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='contact_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='contact_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='image_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='image_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='contact_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='contact_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='image_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='image_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='contact_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='contact_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatna informacija'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='image_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='image_description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis slike'),
        ),
    ]
