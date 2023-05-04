# Generated by Django 4.1.8 on 2023-05-04 11:41

from django.db import migrations
import home.models.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('bulletin_board', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov')), ('notice', wagtail.blocks.TextBlock(label='Obvestilo'))])), ('labs_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('labs', wagtail.blocks.MultipleChoiceBlock(choices=home.models.blocks.get_labs, label='Izpostavljeni laboratoriji'))])), ('news_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('exposed_news', wagtail.blocks.StreamBlock([('news_page', wagtail.blocks.PageChooserBlock(label='Novica', page_type=['news.NewsPage']))]))])), ('events_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('exposed_events', wagtail.blocks.StreamBlock([('event', wagtail.blocks.PageChooserBlock(label='Dogodek', page_type=['events.EventPage']))]))])), ('white_list', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('links', wagtail.blocks.StreamBlock([('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(label='URL')), ('text', wagtail.blocks.TextBlock(label='Ime povezave'))], label='Povezava'))], label='Seznam povezav'))])), ('gallery', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('purple', 'Vijolična'), ('red', 'Rdeča'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov')), ('gallery', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), ('studios', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('studios', wagtail.blocks.MultipleChoiceBlock(choices=home.models.blocks.get_studios, label='Izpostavljeni studii'))])), ('image_embed', wagtail.images.blocks.ImageChooserBlock(label='Slika', template='home/blocks/image_embed.html'))], null=True, use_json_field=False, verbose_name='Telo'),
        ),
    ]
