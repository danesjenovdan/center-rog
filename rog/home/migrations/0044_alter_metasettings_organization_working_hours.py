# Generated by Django 4.1.9 on 2023-07-03 05:53

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0043_alter_basictextpage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metasettings',
            name='organization_working_hours',
            field=wagtail.fields.StreamField([('time', wagtail.blocks.StructBlock([('day', wagtail.blocks.CharBlock(label='Dan')), ('start_time', wagtail.blocks.TimeBlock(label='Začetna ura')), ('end_time', wagtail.blocks.TimeBlock(label='Končna ura'))], label='Dan in ura'))], blank=True, null=True, use_json_field=True, verbose_name='Delovni čas organizacije'),
        ),
    ]
