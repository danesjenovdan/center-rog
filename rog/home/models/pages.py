from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.edit_handlers import MediaChooserPanel

from .base_pages import ObjectProfilePage, ObjectListPage, ObjectArchiveListPage
from .image import CustomImage
from news.models import NewsPage
from events.models import EventPage

import random


def add_see_more_fields(context):
    # random event
    events = list(EventPage.objects.live())
    context["event"] = random.choice(events)
    # random news
    news = list(NewsPage.objects.live())
    context["news"] = random.choice(news)
    # random lab
    labs = list(LabPage.objects.live())
    context["lab"] = random.choice(labs)
    # random studio
    studios = list(StudioPage.objects.live())
    context["studio"] = random.choice(studios)

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
        verbose_name = _("Rezidenca")
        verbose_name_plural = _("Rezidence")

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


class LabPage(ObjectProfilePage):
    thumbnail = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Predogledna slika")
    )
    thumbnail_animation = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Animacija predogledne slike")
    )
    lab_lead = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Vodja laboratorija")
    )

    content_panels = ObjectProfilePage.content_panels + [
        FieldPanel("lab_lead"),
        FieldPanel("thumbnail"),
        MediaChooserPanel("thumbnail_animation"),
        InlinePanel("related_tools", label="Orodja"),
    ]

    parent_page_types = [
        "home.LabListPage"
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

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
        verbose_name = _("Arhiv rezidenc")
        verbose_name_plural = _("Arhivi rezidenc")

ResidenceArchiveListPage._meta.get_field("color_scheme").default = "dark-gray"


### OBJECT LIST PAGES ###

class StudioListPage(ObjectListPage):
    subpage_types = [
        "home.StudioPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["studios"] = StudioPage.objects.child_of(self).live()
        context["archive_page"] = StudioArchiveListPage.objects.live().first()

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Seznam studiev")
        verbose_name_plural = _("Seznami studiev")

StudioListPage._meta.get_field("color_scheme").default = "yellow"


class MarketStoreListPage(ObjectListPage):
    subpage_types = [
        "home.MarketStorePage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["markets"] = MarketStorePage.objects.child_of(self).live()

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Tržnica")
        verbose_name_plural = _("Tržnice")

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
        verbose_name = _("Seznam rezidenc")
        verbose_name_plural = _("Seznami rezidenc")

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
        verbose_name = _("Seznam laboratorijev")
        verbose_name_plural = _("Seznami laboratorijev")

LabListPage._meta.get_field("color_scheme").default = "light-green"
