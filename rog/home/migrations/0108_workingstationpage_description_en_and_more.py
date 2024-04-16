# Generated by Django 4.1.11 on 2024-04-15 11:57

from django.db import migrations, models
import wagtail.blocks
import wagtail.blocks.field_block
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0107_workingstationpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingstationpage',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Kratek opis na kartici'),
        ),
        migrations.AddField(
            model_name='workingstationpage',
            name='description_sl',
            field=models.TextField(blank=True, null=True, verbose_name='Kratek opis na kartici'),
        ),
        migrations.AddField(
            model_name='workingstationpage',
            name='modules_en',
            field=wagtail.fields.StreamField([('bulletpoints', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov', required=False)), ('points', wagtail.blocks.ListBlock(wagtail.blocks.field_block.TextBlock, label='Točka', min=1))], label='Modul s točkami')), ('description', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov', required=False)), ('description', wagtail.blocks.TextBlock(label='Opis'))], label='Modul z opisom')), ('specifications', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov', required=False)), ('points', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('name', wagtail.blocks.TextBlock(label='Specifikacije')), ('value', wagtail.blocks.TextBlock(label='Vrednost'))]), label='Specifikacije', min=1))], label='Modul s specifikacijami'))], blank=True, null=True, use_json_field=True, verbose_name='Moduli'),
        ),
        migrations.AddField(
            model_name='workingstationpage',
            name='modules_sl',
            field=wagtail.fields.StreamField([('bulletpoints', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov', required=False)), ('points', wagtail.blocks.ListBlock(wagtail.blocks.field_block.TextBlock, label='Točka', min=1))], label='Modul s točkami')), ('description', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov', required=False)), ('description', wagtail.blocks.TextBlock(label='Opis'))], label='Modul z opisom')), ('specifications', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov', required=False)), ('points', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('name', wagtail.blocks.TextBlock(label='Specifikacije')), ('value', wagtail.blocks.TextBlock(label='Vrednost'))]), label='Specifikacije', min=1))], label='Modul s specifikacijami'))], blank=True, null=True, use_json_field=True, verbose_name='Moduli'),
        ),
        migrations.AddField(
            model_name='workingstationpage',
            name='tag_en',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Oznaka na kartici'),
        ),
        migrations.AddField(
            model_name='workingstationpage',
            name='tag_sl',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Oznaka na kartici'),
        ),
    ]