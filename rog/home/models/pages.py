from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.edit_handlers import MediaChooserPanel

from .base_pages import BasePage, ObjectProfilePage, ObjectListPage, ObjectArchiveListPage
from .image import CustomImage
from news.models import NewsPage
from events.models import EventPage

import random


def add_see_more_fields(context):
    # random event
    events = list(EventPage.objects.live())
    context["event"] = random.choice(events) if events else None
    # random news
    news = list(NewsPage.objects.live())
    context["news"] = random.choice(news) if news else None
    # random lab
    labs = list(LabPage.objects.live())
    context["lab"] = random.choice(labs) if labs else None
    # random studio
    studios = list(StudioPage.objects.live().filter(archived=False))
    context["studio"] = random.choice(studios) if studios else None

    return context


### OBJECT PROFILE PAGES ###

class StudioPage(ObjectProfilePage):
    thumbnail = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Predogledna slika")
    )

    content_panels = ObjectProfilePage.content_panels + [
        FieldPanel("thumbnail"),
    ]

    parent_page_types = [
        "home.StudioListPage"
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Studio")
        verbose_name_plural = _("Studii")

StudioPage._meta.get_field("color_scheme").default = "yellow"


class ResidencePage(ObjectProfilePage):
    parent_page_types = [
        "home.ResidenceListPage"
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Rezident")
        verbose_name_plural = _("Rezidenti")

ResidencePage._meta.get_field("color_scheme").default = "dark-gray"


class MarketStorePage(ObjectProfilePage):
    card_color_scheme = models.CharField(
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="white",
        verbose_name=_("Barvna shema kartice na seznamu")
    )

    parent_page_types = [
        "home.MarketStoreListPage"
    ]

    content_panels = ObjectProfilePage.content_panels + [
        FieldPanel("card_color_scheme"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Trgovina")
        verbose_name_plural = _("Trgovine")

MarketStorePage._meta.get_field("color_scheme").default = "brown"


class LabPage(BasePage):
    description = models.TextField(blank=True, verbose_name=_("Opis"))
    image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Slika")
    )
    thumbnail = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Predogledna slika")
    )
    gallery = StreamField([
        ("image", blocks.StructBlock([
            ("image", ImageChooserBlock(label=_("Slika"))),
            ("image_description", blocks.TextBlock(label=_("Podnapis k sliki"), max_length=150, required=False))
        ]))
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Galerija"))
    lab_lead = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Vodja laboratorija")
    )
    lab_lead_email = models.EmailField(
        blank=True,
        verbose_name=_("E-mail vodje laboratorija")
    )
    training_dates_link = models.URLField(blank=True, verbose_name=_("Termini usposabljanj"))
    online_trainings_link = models.URLField(blank=True, verbose_name=_("Spletna usposabljanja"))
    optional_button = models.URLField(blank=True, verbose_name=_("Spletna usposabljanja"))
    button = StreamField([
        ("external", blocks.URLBlock(label=_("Zunanji URL"))),
        ("page", blocks.PageChooserBlock(label=_("Podstran"))),
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Gumb"), max_num=1)
    button_text = models.TextField(verbose_name=_("Besedilo na gumbu"), blank=True, null=True)
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("thumbnail"),
        FieldPanel("gallery"),
        FieldPanel("lab_lead"),
        FieldPanel("lab_lead_email"),
        FieldPanel("training_dates_link"),
        FieldPanel("online_trainings_link"),
        FieldPanel("button"),
        FieldPanel("button_text"),
        InlinePanel("related_tools", label="Orodja"),
        FieldPanel("show_see_more_section")
    ]

    parent_page_types = [
        "home.LabListPage"
    ]

    subpage_types = []

    def short_description(self):
        if len(self.description) > 240:
            return self.description[:237] + "..."
        else:
            return self.description

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["object_profile_page_type"] = self.__class__.__name__

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Laboratorij")
        verbose_name_plural = _("Laboratoriji")

LabPage._meta.get_field("color_scheme").default = "light-green"


class LibraryPage(ObjectProfilePage):

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Knjižnica")
        verbose_name_plural = _("Knjižnice")

LibraryPage._meta.get_field("color_scheme").default = "pink"


## OBJECT ARCHIVE LIST PAGES

class StudioArchiveListPage(ObjectArchiveListPage):
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["list"] = StudioPage.objects.live().filter(archived=True)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv studiev")
        verbose_name_plural = _("Arhivi studiev")

StudioArchiveListPage._meta.get_field("color_scheme").default = "yellow"


class ResidenceArchiveListPage(ObjectArchiveListPage):
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["list"] = ResidencePage.objects.live().filter(archived=True)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv rezidentov")
        verbose_name_plural = _("Arhivi rezidentov")

ResidenceArchiveListPage._meta.get_field("color_scheme").default = "dark-gray"


### OBJECT LIST PAGES ###

class StudioListPage(ObjectListPage):
    subpage_types = [
        "home.StudioPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["studios"] = StudioPage.objects.child_of(self).live().filter(archived=False)
        context["archive_page"] = StudioArchiveListPage.objects.live().first()

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Studii")
        verbose_name_plural = _("Studii")

StudioListPage._meta.get_field("color_scheme").default = "yellow"


class MarketStoreListPage(ObjectListPage):
    subpage_types = [
        "home.MarketStorePage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["markets"] = MarketStorePage.objects.child_of(self).live().filter(archived=False)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Market")
        verbose_name_plural = _("Market")

MarketStoreListPage._meta.get_field("color_scheme").default = "brown"


class ResidenceListPage(ObjectListPage):
    subpage_types = [
        "home.ResidencePage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["residents"] = ResidencePage.objects.child_of(self).live().filter(archived=False)
        context["archive_page"] = ResidenceArchiveListPage.objects.live().first()

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Rezidenti")
        verbose_name_plural = _("Rezidenti")

ResidenceListPage._meta.get_field("color_scheme").default = "dark-gray"


class LabListPage(ObjectListPage):
    subpage_types = [
        "home.LabPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["labs"] = LabPage.objects.child_of(self).live()

       # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Laboratoriji")
        verbose_name_plural = _("Laboratoriji")

LabListPage._meta.get_field("color_scheme").default = "light-green"
