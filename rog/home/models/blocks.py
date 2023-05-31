from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .pages import LabPage, LabListPage, StudioPage, StudioListPage, MarketStorePage, MarketStoreListPage, ResidencePage, ResidenceListPage
from news.models import NewsPage, NewsListPage
from events.models import EventPage, EventListPage

import random


class ColoredStructBlock(blocks.StructBlock):
    color = blocks.ChoiceBlock(
        choices=settings.COLOR_SCHEMES,
        label=_("Barva"),
    )

    class Meta:
        abstract = True


class ButtonsBlock(blocks.StreamBlock):
    button = blocks.StructBlock(
        [
            # ('style', blocks.ChoiceBlock(
            #     choices = [
            #         ('underlined', 'Samo podčrtan'),
            #         ('normal', 'Z obrobo'),
            #         ('background', 'Z obrobo in ozadjem')
            #     ],
            #     label=_('Stil gumba'),
            # )),
            # ('arrow', blocks.BooleanBlock(default=False, label=_('Gumb s puščico'), required=False)),
            ('text', blocks.CharBlock("Besedilo na gumbu")),
            # ('function', blocks.ChoiceBlock(
            #     choices = [
            #         ('redirect', 'Povezava na stran'),
            #         ('new_story_modal', 'Odpre okno za oddajo nove zgodbe'),
            #     ],
            #     label=_('Funkcija gumba'),
            # )),
            ('page', blocks.PageChooserBlock(required=False, label="Stran")),
        ],
        label="Gumb",)

    class Meta:
        label = "Gumbi"
        icon = 'snippet'


class BulletinBoardBlock(blocks.StructBlock):
    title = blocks.TextBlock(label=_("Naslov"))
    notice = blocks.TextBlock(label=_("Obvestilo"))
    event = blocks.PageChooserBlock(label=_("Izpostavljen dogodek"), page_type="events.EventPage")
    news = blocks.PageChooserBlock(label=_("Izpostavljena novica"), page_type="news.NewsPage")


    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        # random event (TODO: samo prihajajoči)
        events = list(EventPage.objects.all())
        context["event"] = random.choice(events)
        # random news
        news = list(NewsPage.objects.all())
        context["news"] = random.choice(news)
        # random lab
        labs = list(LabPage.objects.all())
        context["lab"] = random.choice(labs)
        # random markets
        markets = list(MarketStorePage.objects.all())
        context["markets"] = random.sample(markets, 2)
        # random resident
        # residents = list(ResidencePage.objects.all())
        # context["resident"] = random.choice(residents)
        # link to events
        context["events_list"] = EventListPage.objects.all().first()
        # link to news
        context["news_list"] = NewsListPage.objects.all().first()
        # link to studios
        context["studios_list"] = StudioListPage.objects.all().first()
        # link to labs
        context["labs_list"] = LabListPage.objects.all().first()
        # link to markets
        context["markets_list"] = MarketStoreListPage.objects.all().first()
        # link to residences
        context["residents_list"] = ResidenceListPage.objects.all().first()

        return context

    class Meta:
        label = _("Oglasna deska")
        template = "home/blocks/module_bulletin_board.html"


class NewsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    exposed_news = blocks.StreamBlock([
        ("news_page", blocks.PageChooserBlock(
            label=_("Novica"), page_type="news.NewsPage"))
    ])

    class Meta:
        label = _("Izpostavljene novice")
        template = "home/blocks/news_section.html",


class EventsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    exposed_events = blocks.StreamBlock([
        ("event", blocks.PageChooserBlock(
            label=_("Dogodek"), page_type="events.EventPage"))
    ])

    class Meta:
        label = _("Izpostavljeni dogodki")
        template = "home/blocks/events_section.html",


def get_labs():
    return [(lab.id, lab.title) for lab in LabPage.objects.all()]

class LabsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    labs = blocks.MultipleChoiceBlock(label=_("Izpostavljeni laboratoriji"), choices=get_labs)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['labs'] = LabPage.objects.filter(id__in=value["labs"])
        return context

    class Meta:
        label = _("Laboratoriji")
        template = "home/blocks/labs_section.html",


class WhiteListBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    links = blocks.StreamBlock([
        ("link", blocks.StructBlock([
            ("url", blocks.URLBlock(label=_("URL"))),
            ("text", blocks.TextBlock(label=_("Ime povezave"))),
        ], label=_("Povezava")))
    ], label=_("Seznam povezav"))

    class Meta:
        label = _("Seznam povezav")
        template = "home/blocks/white_list_section.html",


class GalleryBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    gallery = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        label = _("Galerija")
        template = "home/blocks/gallery_section.html",


def get_studios():
    return [(studio.id, studio.title) for studio in StudioPage.objects.all()]

class StudiosBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    studios = blocks.MultipleChoiceBlock(label=_("Izpostavljeni studii"), choices=get_studios)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['studios'] = StudioPage.objects.filter(id__in=value["studios"])
        return context

    class Meta:
        label = _("Studii")
        template = "home/blocks/studios_section.html",


class MarketplaceBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    markets = blocks.ListBlock(ColoredStructBlock([
        ('market', blocks.PageChooserBlock(page_type="home.MarketStorePage")),
    ]))

    class Meta:
        label = _("Tržnica")
        template = "home/blocks/marketplace_section.html",


class FullWidthImageBlock(ImageChooserBlock):
    class Meta:
        label = _("Slika")
        template = "home/blocks/image_embed.html",


class ColoredTextBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov"), required=False)
    text = blocks.TextBlock(label=_("Besedilo"))
    image = ImageChooserBlock(label=_("Slika"), required=False)
    image_position = blocks.ChoiceBlock(choices=[
        ("align-left", "Levo"),
        ("align-right", "Desno"),
        ("align-bottom", "Spodaj"),
    ], default="align-bottom", label=_("Pozicija slike"))

    class Meta:
        label = _("Barvno besedilo (s sliko)")
        template = "home/blocks/colored_text_section.html",


# TODO: zbrisi, ko se bodo pocistile migracije
def get_residents():
    return [(resident.id, resident.title) for resident in ResidencePage.objects.all()]

class ResidentsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    residents = blocks.ListBlock(blocks.PageChooserBlock(page_type="home.ResidencePage"), min_num=1, max_num=5)

    class Meta:
        label = _("ROG rezidenti")
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
    residents_section = ResidentsBlock()
    newsletter_section = NewsletterBlock()

    class Meta:
        label = _("Modul")
