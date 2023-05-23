from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from .base_pages import ObjectProfilePage, ObjectListPage


# list pages
class StudioListPage(ObjectListPage):
    subpage_types = [
        'home.StudioPage',
    ]

StudioListPage._meta.get_field('color_scheme').default = 'yellow'


class MarketStoreListPage(ObjectListPage):
    subpage_types = [
        'home.MarketStorePage',
    ]

MarketStoreListPage._meta.get_field('color_scheme').default = 'brown'


class ResidenceListPage(ObjectListPage):
    subpage_types = [
        'home.ResidencePage',
    ]

ResidenceListPage._meta.get_field('color_scheme').default = 'dark-gray'


class LabListPage(ObjectListPage):
    subpage_types = [
        'home.LabPage',
    ]

LabListPage._meta.get_field('color_scheme').default = 'light-green'


# profile pages
class StudioPage(ObjectProfilePage):
    parent_page_types = [
        'home.StudioListPage'
    ]

StudioPage._meta.get_field('color_scheme').default = 'yellow'


class ResidencePage(ObjectProfilePage):
    parent_page_types = [
        'home.ResidenceListPage'
    ]

ResidencePage._meta.get_field('color_scheme').default = 'dark-gray'


class MarketStorePage(ObjectProfilePage):
    parent_page_types = [
        'home.MarketStoreListPage'
    ]

MarketStorePage._meta.get_field('color_scheme').default = 'brown'


class LabPage(ObjectProfilePage):
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    thumbnail_animation = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('thumbnail'),
        FieldPanel('thumbnail_animation'),
    ]

    parent_page_types = [
        'home.LabListPage'
    ]

LabPage._meta.get_field('color_scheme').default = 'light-green'


class LibraryPage(ObjectProfilePage):
    pass

LibraryPage._meta.get_field('color_scheme').default = 'pink'
    