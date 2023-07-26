# Generated by Django 4.1.9 on 2023-07-26 09:27

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_alter_contentpage_body_alter_homepage_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.fields.StreamField([('bulletin_board', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov sekcije')), ('notice', wagtail.blocks.TextBlock(label='Obvestilo')), ('event', wagtail.blocks.PageChooserBlock(label='Izpostavljen dogodek (če pustite prazno, se izbere naključni)', page_type=['events.EventPage'], required=False)), ('news', wagtail.blocks.PageChooserBlock(label='Izpostavljena novica (če pustite prazno, se izbere naključna)', page_type=['news.NewsPage'], required=False))])), ('labs_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('labs', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.LabPage']), label='Izpostavljeni laboratoriji'))])), ('news_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('exposed_news', wagtail.blocks.StreamBlock([('news_page', wagtail.blocks.PageChooserBlock(label='Novica', page_type=['news.NewsPage']))], label='Novice'))])), ('events_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('exposed_events', wagtail.blocks.StreamBlock([('event', wagtail.blocks.PageChooserBlock(label='Dogodek', page_type=['events.EventPage']))], label='Dogodki'))])), ('white_list', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('links', wagtail.blocks.StreamBlock([('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(label='URL')), ('text', wagtail.blocks.TextBlock(label='Ime povezave'))], label='Povezava'))], label='Seznam povezav')), ('button', wagtail.blocks.PageChooserBlock(label='Gumb na dnu sekcije', required=False))])), ('gallery', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('gallery', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), label='Slike')), ('button', wagtail.blocks.PageChooserBlock(label='Gumb na dnu sekcije', required=False))])), ('studios', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('studios', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.StudioPage']), label='Izpostavljeni studii'))])), ('marketplace', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('markets', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(label='Prostor', page_type=['home.MarketStorePage']), label='Izpostavljeni prostori'))])), ('image_embed', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('image', wagtail.images.blocks.ImageChooserBlock(label='Slika')), ('text', wagtail.blocks.TextBlock(blank=True, label='Besedilo (opcijsko)', required=False)), ('link', wagtail.blocks.StreamBlock([('page_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(help_text='Če je prazno, se uporabi naslov strani.', label='Ime', required=False)), ('page', wagtail.blocks.PageChooserBlock(label='Stran'))], label='Povezava do strani')), ('external_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(label='Ime')), ('url', wagtail.blocks.URLBlock(label='URL'))], label='Zunanja povezava'))], label='Povezava pod besedilom', max_num=1, required=False))])), ('colored_text', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov sekcije', required=False)), ('text', wagtail.blocks.TextBlock(label='Besedilo')), ('link', wagtail.blocks.StreamBlock([('page_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(help_text='Če je prazno, se uporabi naslov strani.', label='Ime', required=False)), ('page', wagtail.blocks.PageChooserBlock(label='Stran'))], label='Povezava do strani')), ('external_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(label='Ime')), ('url', wagtail.blocks.URLBlock(label='URL'))], label='Zunanja povezava'))], label='Povezava pod besedilom', max_num=1, required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Slika', required=False)), ('image_position', wagtail.blocks.ChoiceBlock(choices=[('align-left', 'Levo'), ('align-right', 'Desno'), ('align-bottom', 'Spodaj')], label='Pozicija slike'))])), ('colored_text_with_images', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('text', wagtail.blocks.TextBlock(label='Besedilo', required=False)), ('images', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), label='Sličice', max_num=4, min_num=1))])), ('residents_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('residents', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.ResidencePage']), label='Rezidenti', max_num=5, min_num=1))])), ('newsletter_section', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(label='Slika za ozadje'))]))], use_json_field=True, verbose_name='Telo'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('bulletin_board', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Naslov sekcije')), ('notice', wagtail.blocks.TextBlock(label='Obvestilo')), ('event', wagtail.blocks.PageChooserBlock(label='Izpostavljen dogodek (če pustite prazno, se izbere naključni)', page_type=['events.EventPage'], required=False)), ('news', wagtail.blocks.PageChooserBlock(label='Izpostavljena novica (če pustite prazno, se izbere naključna)', page_type=['news.NewsPage'], required=False))])), ('labs_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('labs', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.LabPage']), label='Izpostavljeni laboratoriji'))])), ('news_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('exposed_news', wagtail.blocks.StreamBlock([('news_page', wagtail.blocks.PageChooserBlock(label='Novica', page_type=['news.NewsPage']))], label='Novice'))])), ('events_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('exposed_events', wagtail.blocks.StreamBlock([('event', wagtail.blocks.PageChooserBlock(label='Dogodek', page_type=['events.EventPage']))], label='Dogodki'))])), ('white_list', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('links', wagtail.blocks.StreamBlock([('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(label='URL')), ('text', wagtail.blocks.TextBlock(label='Ime povezave'))], label='Povezava'))], label='Seznam povezav')), ('button', wagtail.blocks.PageChooserBlock(label='Gumb na dnu sekcije', required=False))])), ('gallery', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('gallery', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), label='Slike')), ('button', wagtail.blocks.PageChooserBlock(label='Gumb na dnu sekcije', required=False))])), ('studios', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('studios', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.StudioPage']), label='Izpostavljeni studii'))])), ('marketplace', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('markets', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(label='Prostor', page_type=['home.MarketStorePage']), label='Izpostavljeni prostori'))])), ('image_embed', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('image', wagtail.images.blocks.ImageChooserBlock(label='Slika')), ('text', wagtail.blocks.TextBlock(blank=True, label='Besedilo (opcijsko)', required=False)), ('link', wagtail.blocks.StreamBlock([('page_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(help_text='Če je prazno, se uporabi naslov strani.', label='Ime', required=False)), ('page', wagtail.blocks.PageChooserBlock(label='Stran'))], label='Povezava do strani')), ('external_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(label='Ime')), ('url', wagtail.blocks.URLBlock(label='URL'))], label='Zunanja povezava'))], label='Povezava pod besedilom', max_num=1, required=False))])), ('colored_text', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov sekcije', required=False)), ('text', wagtail.blocks.TextBlock(label='Besedilo')), ('link', wagtail.blocks.StreamBlock([('page_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(help_text='Če je prazno, se uporabi naslov strani.', label='Ime', required=False)), ('page', wagtail.blocks.PageChooserBlock(label='Stran'))], label='Povezava do strani')), ('external_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(label='Ime')), ('url', wagtail.blocks.URLBlock(label='URL'))], label='Zunanja povezava'))], label='Povezava pod besedilom', max_num=1, required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Slika', required=False)), ('image_position', wagtail.blocks.ChoiceBlock(choices=[('align-left', 'Levo'), ('align-right', 'Desno'), ('align-bottom', 'Spodaj')], label='Pozicija slike'))])), ('colored_text_with_images', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], label='Barva')), ('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('text', wagtail.blocks.TextBlock(label='Besedilo', required=False)), ('images', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), label='Sličice', max_num=4, min_num=1))])), ('residents_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Naslov sekcije')), ('intro_text', wagtail.blocks.TextBlock(label='Uvodno besedilo')), ('residents', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.ResidencePage']), label='Rezidenti', max_num=5, min_num=1))])), ('newsletter_section', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(label='Slika za ozadje'))]))], null=True, use_json_field=False, verbose_name='Telo'),
        ),
    ]
