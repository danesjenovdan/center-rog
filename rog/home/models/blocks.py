from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core import validators

from .pages import LabPage, LabListPage, StudioPage, StudioListPage, MarketStorePage, MarketStoreListPage, ResidencePage, ResidenceListPage
from .settings import ExternalLinkBlock, PageLinkBlock
from users.models import MembershipType
from news.models import NewsPage, NewsListPage
from events.models import EventPage, EventListPage

import random
from datetime import date


class ModuleBlock(blocks.StructBlock):
    show_link_in_secondary_menu = blocks.BooleanBlock(
        required=False,
        label=_("Pokaži povezavo do modula v sekundarnem meniju")
    )

    class Meta:
        abstract = True


class ColoredStructBlock(ModuleBlock):
    color = blocks.ChoiceBlock(
        choices=settings.COLOR_SCHEMES,
        label=_("Barva"),
    )
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava pod besedilom"))

    class Meta:
        abstract = True


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
            context["events"] = [value["event"]]
        else:
            upcoming_events = EventPage.objects.live().filter(start_day__gte=today).order_by("-first_published_at")
            used_categories = set()
            events = list()
            for event in upcoming_events:
                if event.category not in used_categories:
                    events.append(event)
                    used_categories.add(event.category)
                if len(events) >= 1:
                    break
            context["events"] = events
        # link to all events
        context["events_list"] = EventListPage.objects.live().first()

        # random news
        if value["news"] is not None:
            context["news"] = [value["news"]]
        else:
            news = NewsPage.objects.live().order_by("-first_published_at")[:1]
            context["news"] = news
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
    ], max_num=10, blank=True, required=False, label=_("Novice"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava/gumb na dnu (opcijsko)"))

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
    ], max_num=10, blank=True, required=False, label=_("Dogodki"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava/gumb na dnu (opcijsko)"))

    class Meta:
        label = _("Izpostavljeni dogodki")
        template = "home/blocks/events_section.html",


def get_labs():
    return [(lab.id, lab.title) for lab in LabPage.objects.all()]

class LabsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    labs = blocks.ListBlock(blocks.PageChooserBlock(page_type="home.LabPage"), label=_("Izpostavljeni laboratoriji"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava/gumb na dnu (opcijsko)"))

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
            ("url", blocks.URLBlock(label=_("URL"), required=False)),
            ("text", blocks.TextBlock(label=_("Ime povezave"))),
        ], label=_("Povezava")))
    ], label=_("Seznam povezav"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava/gumb na dnu (opcijsko)"))

    class Meta:
        label = _("Seznam povezav")
        template = "home/blocks/white_list_section.html",


class GalleryBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"), required=False)
    gallery = blocks.ListBlock(blocks.StructBlock([
        ("image", ImageChooserBlock(label=_("Slika"))),
        ("image_description", blocks.TextBlock(label=_("Podnapis k sliki"), max_length=150, required=False))
    ]), label=_("Galerija"))

    class Meta:
        label = _("Galerija")
        template = "home/blocks/gallery_section.html",


def get_studios():
    return [(studio.id, studio.title) for studio in StudioPage.objects.all()]

class StudiosBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    studios = blocks.ListBlock(
        blocks.PageChooserBlock(page_type="home.StudioPage"),
        max_num=10, label=_("Izpostavljeni studii"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava/gumb na dnu (opcijsko)"))

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
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava/gumb na dnu (opcijsko)"))

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


    class Meta:
        label = _("Slika")
        template = "home/blocks/image_embed.html",


class ColoredTextBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"), required=False)
    text = blocks.TextBlock(label=_("Besedilo"))
    image = ImageChooserBlock(label=_("Slika"), required=False)
    image_description = blocks.TextBlock(label=_("Opis pod sliko"), blank=True, required=False)
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


class ColoredTextCardsBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    text = blocks.TextBlock(label=_("Besedilo"), required=False)
    cards = blocks.ListBlock(blocks.StructBlock([
        ("image", ImageChooserBlock()),
        ("description", blocks.TextBlock(label=_("Opis pod sliko"))),
        ("link", blocks.URLBlock(label=_("Povezava"), required=False)),
        ("link_text", blocks.TextBlock(label=_("Ime povezave"), required=False)),
    ]), label=_("Kartice"), min_num=1)

    class Meta:
        label = _("Barvno besedilo s karticami")
        template = "home/blocks/colored_text_with_cards_section.html"


class ColoredRichTextBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    rich_text = blocks.RichTextBlock(label=_("Besedilo"))

    class Meta:
        label = _("Barvno obogateno besedilo")
        template = "home/blocks/colored_rich_text_section.html"


class ContactsListBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    contacts = blocks.ListBlock(blocks.StructBlock([
        ("name", blocks.TextBlock(label=_("Ime"))),
        ("position", blocks.TextBlock(label=_("Delovno mesto"))),
        ("email", blocks.EmailBlock(label=_("Elektronski naslov")))
    ]), label=_("Kontakti"))

    class Meta:
        label = _("Kontakti")
        template = "home/blocks/contacts_section.html",


# TODO: zbrisi, ko se bodo pocistile migracije
def get_residents():
    return [(resident.id, resident.title) for resident in ResidencePage.objects.all()]

class ResidentsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))
    intro_text = blocks.TextBlock(label=_("Uvodno besedilo"))
    residents = blocks.ListBlock(blocks.PageChooserBlock(page_type="home.ResidencePage"), min_num=1, max_num=5, label=_("Rezidenti"))
    link = blocks.StreamBlock([
        ("page_link", PageLinkBlock(label=_("Povezava do strani"))),
        ("external_link", ExternalLinkBlock(label=_("Zunanja povezava"))),
    ], max_num=1, blank=True, required=False, label=_("Povezava/gumb na dnu (opcijsko)"))

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
        template = "home/blocks/newsletter_section.html"


class MembershipsBlock(ColoredStructBlock):
    title = blocks.CharBlock(label=_("Naslov sekcije"))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["membership_types"] = MembershipType.objects.all()
        return context

    class Meta:
        label = _("Vrste članstev")
        template = "home/blocks/memberships_section.html"


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
    colored_text_with_cards = ColoredTextCardsBlock()
    colored_rich_text = ColoredRichTextBlock()
    contacts_section = ContactsListBlock()
    memberships_section = MembershipsBlock()
    residents_section = ResidentsBlock()
    newsletter_section = NewsletterBlock()

    class Meta:
        label = _("Modul")
