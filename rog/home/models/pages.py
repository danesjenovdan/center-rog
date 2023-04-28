from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


from .blocks import (ModuleBlock)


class HomePage(Page):
    body = StreamField(
        ModuleBlock(),
        verbose_name="Telo",
        null=True,
        use_json_field=False
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    subpage_types = [
        'home.StudioListPage',
        'home.MarketStoreListPage',
        'home.ResidenceListPage',
        'home.LabListPage',
        'home.ContentPage',
        'events.EventListPage',
        'events.EventListArchivePage',
        'news.NewsListPage',
        'news.NewsListArchivePage'
    ]


class BasePage(Page):
    color_scheme = models.CharField(
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="white",
    )

    class Meta:
        abstract = True


class ObjectListPage(BasePage):
    intro_text = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
    ]

    class Meta:
        abstract = True


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


class ObjectProfilePage(BasePage):
    description = models.TextField(blank=True)
    # contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    link_1 = models.URLField(blank=True)
    link_2 = models.URLField(blank=True)
    link_3 = models.URLField(blank=True)
    contact_description = models.TextField(blank=True)
    # working hours
    working_hours = StreamField([
        ('time', blocks.StructBlock([
            ('day', blocks.CharBlock(label=_('Dan'))),
            ('start_time', blocks.TimeBlock(label=_('Začetna ura'))),
            ('end_time', blocks.TimeBlock(label=_('Končna ura'))),
        ], label=_('Dan in ura')))
    ], blank=True, null=True, use_json_field=False)
    # gallery
    # gallery = StreamField(
    #     blocks.ListBlock(ImageChooserBlock()),
    #     blank=True,
    #     null=True,
    #     use_json_field=False
    # )
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        MultiFieldPanel(
            [
                FieldPanel('email'),
                FieldPanel('phone'),
                FieldPanel('link_1'),
                FieldPanel('link_2'),
                FieldPanel('link_3'),
                FieldPanel('contact_description'),
            ],
            heading=_('Kontaktni podatki')
        ),
        FieldPanel('working_hours'),
    ]

    subpage_types = []

    class Meta:
        abstract = True


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
    parent_page_types = [
        'home.LabListPage'
    ]

LabPage._meta.get_field('color_scheme').default = 'light-green'


class LibraryPage(ObjectProfilePage):
    pass

LibraryPage._meta.get_field('color_scheme').default = 'pink'

class ContentPage(BasePage):
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel('color_scheme'),
    ]
    