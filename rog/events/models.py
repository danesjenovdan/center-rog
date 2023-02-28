from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class EventPage(Page):
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
        FieldPanel('long_description'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
    ]


class EventListPage(Page):
    pass


class EventListArchivePage(Page):
    pass
