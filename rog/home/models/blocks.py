from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .pages import LabPage
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
    labs = blocks.MultipleChoiceBlock(label=_("Izpostavljeni laboratoriji"), choices=get_labs, required=True)

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


class ModuleBlock(blocks.StreamBlock):
    bulletin_board = BulletinBoardBlock()
    labs_section = LabsBlock()
    news_section = NewsBlock()
    events_section = EventsBlock()
    white_list = WhiteListBlock()
    gallery = GalleryBlock()
    image_embed = ImageChooserBlock(
        label=_("Slika"), template="home/blocks/image_embed.html"
    )

    class Meta:
        label = _("Modul")
