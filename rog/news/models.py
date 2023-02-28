from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class NewsPage(Page):
    short_description = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
    ]


class NewsListPage(Page):
    pass


class NewsListArchivePage(Page):
    pass
