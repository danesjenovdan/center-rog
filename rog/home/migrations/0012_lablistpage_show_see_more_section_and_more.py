# Generated by Django 4.1.9 on 2023-05-31 20:23

from django.db import migrations, models
import home.models.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='lablistpage',
            name='show_see_more_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='marketstorelistpage',
            name='show_see_more_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='residencelistpage',
            name='show_see_more_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studiolistpage',
            name='show_see_more_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('bulletin_board', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov')), ('notice', wagtail.blocks.TextBlock(label='Obvestilo')), ('event', wagtail.blocks.PageChooserBlock(label='Izpostavljen dogodek', page_type=['events.EventPage'])), ('news', wagtail.blocks.PageChooserBlock(label='Izpostavljena novica', page_type=['news.NewsPage']))])), ('labs_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('labs', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.LabPage']), label='Izpostavljeni laboratoriji', max_num=5, min_num=1))])), ('news_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('exposed_news', wagtail.blocks.StreamBlock([('news_page', wagtail.blocks.PageChooserBlock(label='Novica', page_type=['news.NewsPage']))]))])), ('events_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('exposed_events', wagtail.blocks.StreamBlock([('event', wagtail.blocks.PageChooserBlock(label='Dogodek', page_type=['events.EventPage']))]))])), ('white_list', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('links', wagtail.blocks.StreamBlock([('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(label='URL')), ('text', wagtail.blocks.TextBlock(label='Ime povezave'))], label='Povezava'))], label='Seznam povezav'))])), ('gallery', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('purple', 'Vijolična'), ('red', 'Rdeča'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov')), ('gallery', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), ('studios', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('studios', wagtail.blocks.MultipleChoiceBlock(choices=home.models.blocks.get_studios, label='Izpostavljeni studii'))])), ('marketplace', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('markets', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('purple', 'Vijolična'), ('red', 'Rdeča'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('market', wagtail.blocks.PageChooserBlock(page_type=['home.MarketStorePage']))])))])), ('image_embed', home.models.blocks.FullWidthImageBlock()), ('colored_text', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('purple', 'Vijolična'), ('red', 'Rdeča'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov', required=False)), ('text', wagtail.blocks.TextBlock(label='Besedilo')), ('image', wagtail.images.blocks.ImageChooserBlock(label='Slika', required=False)), ('image_position', wagtail.blocks.ChoiceBlock(choices=[('align-left', 'Levo'), ('align-right', 'Desno'), ('align-bottom', 'Spodaj')], label='Pozicija slike'))])), ('residents_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('residents', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.ResidencePage']), max_num=5, min_num=1))])), ('newsletter_section', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(label='Slika za ozadje'))]))], null=True, use_json_field=False, verbose_name='Telo'),
        ),
    ]
