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


class ObjectListPage(Page):
    intro_text = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
    ]


class ObjectProfilePage(Page):
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