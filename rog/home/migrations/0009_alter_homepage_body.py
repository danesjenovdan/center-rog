# Generated by Django 4.1.7 on 2023-03-02 16:23

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StreamBlock([('body', wagtail.blocks.StreamBlock([('box_emphasized', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('text', wagtail.blocks.RichTextBlock(label='Besedilo', required=False)), ('buttons', wagtail.blocks.StreamBlock([('button', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock('Besedilo na gumbu')), ('page', wagtail.blocks.PageChooserBlock(label='Stran', required=False))], label='Gumb'))], label='Gumbi', required=False))], icon='title', label='Poudarjeno besedilo z okvirjem', template='home/blocks/box_emphasized.html')), ('news_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('text', wagtail.blocks.RichTextBlock(label='Besedilo', required=False)), ('buttons', wagtail.blocks.StreamBlock([('button', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock('Besedilo na gumbu')), ('page', wagtail.blocks.PageChooserBlock(label='Stran', required=False))], label='Gumb'))], label='Gumbi', required=False))], icon='title', label='Poudarjeno besedilo z okvirjem', template='home/blocks/box_emphasized.html'))], required=False))]))], default='', use_json_field=False, verbose_name='Telo'),
        ),
    ]
