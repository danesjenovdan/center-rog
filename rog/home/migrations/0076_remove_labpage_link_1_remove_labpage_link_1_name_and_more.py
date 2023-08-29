# Generated by Django 4.1.10 on 2023-08-28 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0075_labpage_link_1_name_labpage_link_2_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labpage',
            name='link_1',
        ),
        migrations.RemoveField(
            model_name='labpage',
            name='link_1_name',
        ),
        migrations.RemoveField(
            model_name='labpage',
            name='link_2',
        ),
        migrations.RemoveField(
            model_name='labpage',
            name='link_2_name',
        ),
        migrations.RemoveField(
            model_name='labpage',
            name='link_3',
        ),
        migrations.RemoveField(
            model_name='labpage',
            name='link_3_name',
        ),
        migrations.RemoveField(
            model_name='librarypage',
            name='link_1',
        ),
        migrations.RemoveField(
            model_name='librarypage',
            name='link_1_name',
        ),
        migrations.RemoveField(
            model_name='librarypage',
            name='link_2',
        ),
        migrations.RemoveField(
            model_name='librarypage',
            name='link_2_name',
        ),
        migrations.RemoveField(
            model_name='librarypage',
            name='link_3',
        ),
        migrations.RemoveField(
            model_name='librarypage',
            name='link_3_name',
        ),
        migrations.RemoveField(
            model_name='marketstorepage',
            name='link_1',
        ),
        migrations.RemoveField(
            model_name='marketstorepage',
            name='link_1_name',
        ),
        migrations.RemoveField(
            model_name='marketstorepage',
            name='link_2',
        ),
        migrations.RemoveField(
            model_name='marketstorepage',
            name='link_2_name',
        ),
        migrations.RemoveField(
            model_name='marketstorepage',
            name='link_3',
        ),
        migrations.RemoveField(
            model_name='marketstorepage',
            name='link_3_name',
        ),
        migrations.RemoveField(
            model_name='residencepage',
            name='link_1',
        ),
        migrations.RemoveField(
            model_name='residencepage',
            name='link_1_name',
        ),
        migrations.RemoveField(
            model_name='residencepage',
            name='link_2',
        ),
        migrations.RemoveField(
            model_name='residencepage',
            name='link_2_name',
        ),
        migrations.RemoveField(
            model_name='residencepage',
            name='link_3',
        ),
        migrations.RemoveField(
            model_name='residencepage',
            name='link_3_name',
        ),
        migrations.RemoveField(
            model_name='studiopage',
            name='link_1',
        ),
        migrations.RemoveField(
            model_name='studiopage',
            name='link_1_name',
        ),
        migrations.RemoveField(
            model_name='studiopage',
            name='link_2',
        ),
        migrations.RemoveField(
            model_name='studiopage',
            name='link_2_name',
        ),
        migrations.RemoveField(
            model_name='studiopage',
            name='link_3',
        ),
        migrations.RemoveField(
            model_name='studiopage',
            name='link_3_name',
        ),
        migrations.AddField(
            model_name='labpage',
            name='facebook',
            field=models.URLField(blank=True, verbose_name='Facebook link'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='instagram',
            field=models.URLField(blank=True, verbose_name='Instagram link'),
        ),
        migrations.AddField(
            model_name='labpage',
            name='website',
            field=models.URLField(blank=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='facebook',
            field=models.URLField(blank=True, verbose_name='Facebook link'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='instagram',
            field=models.URLField(blank=True, verbose_name='Instagram link'),
        ),
        migrations.AddField(
            model_name='librarypage',
            name='website',
            field=models.URLField(blank=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='facebook',
            field=models.URLField(blank=True, verbose_name='Facebook link'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='instagram',
            field=models.URLField(blank=True, verbose_name='Instagram link'),
        ),
        migrations.AddField(
            model_name='marketstorepage',
            name='website',
            field=models.URLField(blank=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='facebook',
            field=models.URLField(blank=True, verbose_name='Facebook link'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='instagram',
            field=models.URLField(blank=True, verbose_name='Instagram link'),
        ),
        migrations.AddField(
            model_name='residencepage',
            name='website',
            field=models.URLField(blank=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='facebook',
            field=models.URLField(blank=True, verbose_name='Facebook link'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='instagram',
            field=models.URLField(blank=True, verbose_name='Instagram link'),
        ),
        migrations.AddField(
            model_name='studiopage',
            name='website',
            field=models.URLField(blank=True, verbose_name='Website'),
        ),
    ]