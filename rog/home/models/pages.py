from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    pass


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