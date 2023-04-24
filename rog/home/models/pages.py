from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from .blocks import (SectionBlock)


class HomePage(Page):
    body = StreamField(
        [('section', SectionBlock())],
        verbose_name="Telo",
        default='',
        use_json_field=False
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


class BasePage(Page):
    COLOR_SCHEMES = [
        ("brown", "Rjava"),
        ("light-gray", "Svetlo siva"),
        ("dark-gray", "Temno siva"),
        ("light-blue", "Svetlo modra"),
        ("dark-blue", "Temno modra"),
        ("light-green", "Svetlo zelena"),
        ("dark-green", "Temno zelena"),
        ("purple", "Vijolična"),
        ("red", "Rdeča"),
        ("orange", "Oranžna"),
        ("pink", "Roza"),
        ("yellow", "Rumena"),
        ("white", "Bela"),
    ]
    
    color_scheme = models.CharField(
        max_length=20,
        choices=COLOR_SCHEMES,
        default="white",
    )

    content_panels = Page.content_panels + [
        FieldPanel('color_scheme'),
    ]


class ObjectListPage(BasePage):
    intro_text = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
    ]


class ObjectProfilePage(BasePage):
    description = models.TextField(blank=True)


class StudioPage(ObjectProfilePage):
    pass


class ResidencePage(ObjectProfilePage):
    pass


class MarketStorePage(ObjectProfilePage):
    pass


class LibraryPage(ObjectProfilePage):
    pass


class ContentPage(Page):
    pass