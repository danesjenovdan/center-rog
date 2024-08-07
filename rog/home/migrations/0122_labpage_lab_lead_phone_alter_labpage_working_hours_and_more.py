# Generated by Django 4.1.11 on 2024-08-01 16:43

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0121_remove_librarypage_archived_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='labpage',
            name='lab_lead_phone',
            field=models.TextField(blank=True, verbose_name='Telefonska številka vodje laboratorija'),
        ),
        migrations.AlterField(
            model_name='labpage',
            name='working_hours',
            field=wagtail.fields.StreamField([('time', wagtail.blocks.StructBlock([('day', wagtail.blocks.CharBlock(label='Dan')), ('start_time', wagtail.blocks.TimeBlock(label='Začetna ura')), ('end_time', wagtail.blocks.TimeBlock(label='Končna ura'))], label='Dan in ura')), ('notice', wagtail.blocks.StructBlock([('day', wagtail.blocks.CharBlock(label='Dan')), ('text', wagtail.blocks.CharBlock(label='Opomba'))], label='Dan in opomba'))], blank=True, null=True, use_json_field=True, verbose_name='Delovni čas'),
        ),
        migrations.AlterField(
            model_name='labpage',
            name='working_hours_en',
            field=wagtail.fields.StreamField([('time', wagtail.blocks.StructBlock([('day', wagtail.blocks.CharBlock(label='Dan')), ('start_time', wagtail.blocks.TimeBlock(label='Začetna ura')), ('end_time', wagtail.blocks.TimeBlock(label='Končna ura'))], label='Dan in ura')), ('notice', wagtail.blocks.StructBlock([('day', wagtail.blocks.CharBlock(label='Dan')), ('text', wagtail.blocks.CharBlock(label='Opomba'))], label='Dan in opomba'))], blank=True, null=True, use_json_field=True, verbose_name='Delovni čas'),
        ),
        migrations.AlterField(
            model_name='labpage',
            name='working_hours_sl',
            field=wagtail.fields.StreamField([('time', wagtail.blocks.StructBlock([('day', wagtail.blocks.CharBlock(label='Dan')), ('start_time', wagtail.blocks.TimeBlock(label='Začetna ura')), ('end_time', wagtail.blocks.TimeBlock(label='Končna ura'))], label='Dan in ura')), ('notice', wagtail.blocks.StructBlock([('day', wagtail.blocks.CharBlock(label='Dan')), ('text', wagtail.blocks.CharBlock(label='Opomba'))], label='Dan in opomba'))], blank=True, null=True, use_json_field=True, verbose_name='Delovni čas'),
        ),
        migrations.AlterField(
            model_name='librarypage',
            name='active_from',
            field=models.DateField(blank=True, null=True, verbose_name='Začetek delovanja'),
        ),
        migrations.AlterField(
            model_name='librarypage',
            name='active_to',
            field=models.DateField(blank=True, null=True, verbose_name='Konec delovanja (po tem datumu bo avtomatsko arhiviran)'),
        ),
        migrations.AlterField(
            model_name='librarypage',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Arhiviraj? (brez določitve datuma)'),
        ),
        migrations.AlterField(
            model_name='marketstorepage',
            name='active_from',
            field=models.DateField(blank=True, null=True, verbose_name='Začetek delovanja'),
        ),
        migrations.AlterField(
            model_name='marketstorepage',
            name='active_to',
            field=models.DateField(blank=True, null=True, verbose_name='Konec delovanja (po tem datumu bo avtomatsko arhiviran)'),
        ),
        migrations.AlterField(
            model_name='marketstorepage',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Arhiviraj? (brez določitve datuma)'),
        ),
        migrations.AlterField(
            model_name='residencepage',
            name='active_from',
            field=models.DateField(blank=True, null=True, verbose_name='Začetek delovanja'),
        ),
        migrations.AlterField(
            model_name='residencepage',
            name='active_to',
            field=models.DateField(blank=True, null=True, verbose_name='Konec delovanja (po tem datumu bo avtomatsko arhiviran)'),
        ),
        migrations.AlterField(
            model_name='residencepage',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Arhiviraj? (brez določitve datuma)'),
        ),
        migrations.AlterField(
            model_name='studiopage',
            name='active_from',
            field=models.DateField(blank=True, null=True, verbose_name='Začetek delovanja'),
        ),
        migrations.AlterField(
            model_name='studiopage',
            name='active_to',
            field=models.DateField(blank=True, null=True, verbose_name='Konec delovanja (po tem datumu bo avtomatsko arhiviran)'),
        ),
        migrations.AlterField(
            model_name='studiopage',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Arhiviraj? (brez določitve datuma)'),
        ),
    ]
