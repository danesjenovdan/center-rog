# Generated by Django 4.1.10 on 2023-08-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0074_alter_labpage_image_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='labpage',
            name='link_1_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='link_2_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='link_3_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='link_1_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='link_2_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='link_3_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='link_1_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='link_2_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='link_3_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='link_1_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='link_2_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='link_3_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='link_1_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='link_2_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='link_3_name',
            field=models.TextField(blank=True, verbose_name='Ime povezave'),
        ),
    ]
