# Generated by Django 4.1.7 on 2023-03-03 13:16

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    replaces = [('home', '0005_homepage_body'), ('home', '0006_alter_homepage_body'), ('home', '0007_alter_homepage_body'), ('home', '0008_alter_homepage_body'), ('home', '0009_alter_homepage_body'), ('home', '0010_alter_homepage_body'), ('home', '0011_alter_homepage_body'), ('home', '0012_alter_homepage_body')]

    dependencies = [
        ('home', '0004_contentpage_objectlistpage_objectprofilepage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StructBlock([('body', wagtail.blocks.StreamBlock([('box_emphasized', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('text', wagtail.blocks.RichTextBlock(label='Besedilo', required=False)), ('buttons', wagtail.blocks.StreamBlock([('button', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock('Besedilo na gumbu')), ('page', wagtail.blocks.PageChooserBlock(label='Stran', required=False))], label='Gumb'))], label='Gumbi', required=False))], icon='title', label='Poudarjeno besedilo z okvirjem', template='home/blocks/box_emphasized.html')), ('news_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('news', wagtail.blocks.StreamBlock([('news_page', wagtail.blocks.PageChooserBlock(label='Stran', page_type=['news.NewsPage'], required=False))], label='Novice'))], icon='title', label='Izpostavljene novice', template='home/blocks/news_section.html')), ('image_embed', wagtail.images.blocks.ImageChooserBlock(label='Slika', template='home/blocks/image_embed.html'))], label='Vsebina', required=False))]))], default='', use_json_field=False, verbose_name='Telo'),
        ),
    ]
