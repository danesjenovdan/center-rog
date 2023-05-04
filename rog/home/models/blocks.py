from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .pages import LabPage, StudioPage, MarketStorePage
from news.models import NewsPage
from events.models import EventPage


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

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        # exposed event
        context["event"] = EventPage.objects.all().first()
        # exposed news
        context["news"] = NewsPage.objects.all().first()
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


def get_markets():
    return [(market.id, market.title) for market in MarketStorePage.objects.all()]

class MarketplaceBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    markets = blocks.MultipleChoiceBlock(label=_("Trgovine"), choices=get_markets)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["markets"] = MarketStorePage.objects.filter(id__in=value["markets"])
        return context

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

    class Meta:
        label = _("Barvno besedilo (s sliko)")
        template = "home/blocks/colored_text_section.html",


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

    class Meta:
        label = _("Modul")
