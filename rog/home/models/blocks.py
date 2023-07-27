from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .pages import LabPage, LabListPage, StudioPage, StudioListPage, MarketStorePage, MarketStoreListPage, ResidencePage, ResidenceListPage
from .settings import ExternalLinkBlock, PageLinkBlock
from news.models import NewsPage, NewsListPage
from events.models import EventPage, EventListPage

import random
from datetime import date


class ColoredStructBlock(blocks.StructBlock):
    color = blocks.ChoiceBlock(
        choices=settings.COLOR_SCHEMES,
        label=_("Barva"),
    )

    class Meta:
        abstract = True


class ButtonBlock(blocks.StructBlock):
    button = blocks.PageChooserBlock(label=_("Povezava"))
    button_text = blocks.TextBlock(label=_("Ime gumba"))


class LinkBlock(blocks.StructBlock):
    link = blocks.URLBlock(label=_("Povezava"))
    link_text = blocks.TextBlock(label=_("Ime povezave"))


class BulletinBoardBlock(blocks.StructBlock):
    title = blocks.TextBlock(label=_("Naslov sekcije"))
    notice = blocks.TextBlock(label=_("Obvestilo"))
    event = blocks.PageChooserBlock(label=_("Izpostavljen dogodek (če pustite prazno, se izbere naključni)"), page_type="events.EventPage", required=False)
    news = blocks.PageChooserBlock(label=_("Izpostavljena novica (če pustite prazno, se izbere naključna)"), page_type="news.NewsPage", required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        # random event
        today = date.today()
        if value["event"] is not None:
            context["event"] = value["event"]
        else:
            upcoming_events = list(EventPage.objects.live().filter(start_day__gte=today))
            if len(upcoming_events) > 0:
                context["event"] = random.choice(upcoming_events)
        # link to all events
        context["events_list"] = EventListPage.objects.live().first()

        # random news
        if value["news"] is not None:
            context["news"] = value["news"]
        else:
            news = list(NewsPage.objects.live())
            if len(news) > 0:
                context["news"] = random.choice(news)
        # link to news
        context["news_list"] = NewsListPage.objects.live().first()

        # random lab
        labs = list(LabPage.objects.live())
        if len(labs) > 0:
            context["lab"] = random.choice(labs)
        # link to labs
        context["labs_list"] = LabListPage.objects.live().first()

        # random markets
        markets = list(MarketStorePage.objects.live())
        if len(markets) > 1:
            context["markets"] = random.sample(markets, 2)
        elif len(markets) > 0:
            context["markets"] = random.sample(markets, 1)            
        # link to markets
        context["markets_list"] = MarketStoreListPage.objects.live().first()
        
        # link to studios
        context["studios_list"] = StudioListPage.objects.live().first()
        
        # link to residences
        context["residents_list"] = ResidenceListPage.objects.live().first()

        return context

    class Meta:
        label = _("Oglasna deska")
        template = "home/blocks/bulletin_board.html"


class NewsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    exposed_news = blocks.StreamBlock([
        ("news_page", blocks.PageChooserBlock(
            label=_("Novica"), page_type="news.NewsPage"))
    ], label=_("Novice"))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["news_list"] = NewsListPage.objects.live().first()
        return context

    class Meta:
        label = _("Izpostavljene novice")
        template = "home/blocks/news_section.html",


class EventsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    exposed_events = blocks.StreamBlock([
        ("event", blocks.PageChooserBlock(
            label=_("Dogodek"), page_type="events.EventPage"))
    ], label=_("Dogodki"))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["events_list"] = EventListPage.objects.live().first()
        return context

    class Meta:
        label = _("Izpostavljeni dogodki")
        template = "home/blocks/events_section.html",


def get_labs():
    return [(lab.id, lab.title) for lab in LabPage.objects.all()]

class LabsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    labs = blocks.ListBlock(blocks.PageChooserBlock(page_type="home.LabPage"), label=_("Izpostavljeni laboratoriji"))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["labs_list"] = LabListPage.objects.live().first()
        return context

    class Meta:
        label = _("Laboratoriji")
        template = "home/blocks/labs_section.html",


class WhiteListBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    links = blocks.StreamBlock([
        ("link", blocks.StructBlock([
            ("url", blocks.URLBlock(label=_("URL"))),
            ("text", blocks.TextBlock(label=_("Ime povezave"))),
        ], label=_("Povezava")))
    ], label=_("Seznam povezav"))
    button = blocks.PageChooserBlock(required=False, label=_("Gumb na dnu sekcije"))

    class Meta:
        label = _("Seznam povezav")
        template = "home/blocks/white_list_section.html",


class GalleryBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    gallery = blocks.ListBlock(ImageChooserBlock(), label=_("Slike"))
    button = blocks.PageChooserBlock(required=False, label=_("Gumb na dnu sekcije"))

    class Meta:
        label = _("Galerija")
        template = "home/blocks/gallery_section.html",


def get_studios():
    return [(studio.id, studio.title) for studio in StudioPage.objects.all()]

class StudiosBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    studios = blocks.ListBlock(blocks.PageChooserBlock(page_type="home.StudioPage"), label=_("Izpostavljeni studii"))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["studios_list"] = StudioListPage.objects.live().first()
        return context

    class Meta:
        label = _("Studii")
        template = "home/blocks/studios_section.html",


class MarketplaceBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    markets = blocks.ListBlock(blocks.PageChooserBlock(page_type="home.MarketStorePage", label=_("Prostor")), label=_("Izpostavljeni prostori"))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["markets_list"] = MarketStoreListPage.objects.live().first()
        return context

    class Meta:
        label = _("Tržnica")
        template = "home/blocks/marketplace_section.html",


class FullWidthImageBlock(ColoredStructBlock):
    image = ImageChooserBlock(label=_("Slika"))
    text = blocks.TextBlock(label=_("Besedilo (opcijsko)"), blank=True, required=False)
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava pod besedilom"))
    
    class Meta:
        label = _("Slika")
        template = "home/blocks/image_embed.html",


class ColoredTextBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"), required=False)
    text = blocks.TextBlock(label=_("Besedilo"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, required=False, label=_("Povezava pod besedilom"))
    image = ImageChooserBlock(label=_("Slika"), required=False)
    image_position = blocks.ChoiceBlock(choices=[
        ("align-left", "Levo"),
        ("align-right", "Desno"),
        ("align-bottom", "Spodaj"),
    ], default="align-bottom", label=_("Pozicija slike"))

    class Meta:
        label = _("Barvno besedilo (s sliko)")
        template = "home/blocks/colored_text_section.html"


class ColoredTextSmallImagesBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    text = blocks.TextBlock(label=_("Besedilo"), required=False)
    images = blocks.ListBlock(blocks.StructBlock([
        ("image", ImageChooserBlock()),
        ("link", blocks.URLBlock(label=_("Povezava"), required=False))
    ]), label=_("Sličice"), min_num=1, max_num=4)

    class Meta:
        label = _("Barvno besedilo z majhnimi slikami")
        template = "home/blocks/colored_text_with_images_section.html"


class ColoredRichTextBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    rich_text = blocks.RichTextBlock(label=_("Besedilo"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], required=False, min_num=0, max_num=1, label=_("Povezava/gumb na dnu (opcijsko)"))
    
    class Meta:
        label = _("Barvno obogateno besedilo")
        template = "home/blocks/colored_rich_text_section.html",


# TODO: zbrisi, ko se bodo pocistile migracije
def get_residents():
    return [(resident.id, resident.title) for resident in ResidencePage.objects.all()]

class ResidentsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    residents = blocks.ListBlock(blocks.PageChooserBlock(page_type="home.ResidencePage"), min_num=1, max_num=5, label=_("Rezidenti"))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["residents_list"] = ResidenceListPage.objects.live().first()
        return context

    class Meta:
        label = _("Rezidenti")
        template = "home/blocks/residents_section.html",


class NewsletterBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(label = _("Slika za ozadje"))

    class Meta:
        label = _("Novičnik")
        template = "home/blocks/newsletter_section.html",


class ModuleBlock(blocks.StreamBlock):
    bulletin_board = BulletinBoardBlock()
    labs_section = LabsBlock()
    news_section = NewsBlock()
    events_section = EventsBlock()
    white_list = WhiteListBlock()
    gallery = GalleryBlock()
    studios = StudiosBlock()
    marketplace = MarketplaceBlock()
    image_embed = FullWidthImageBlock()
    colored_text = ColoredTextBlock()
    colored_text_with_images = ColoredTextSmallImagesBlock()
    colored_rich_text = ColoredRichTextBlock()
    residents_section = ResidentsBlock()
    newsletter_section = NewsletterBlock()

    class Meta:
        label = _("Modul")
