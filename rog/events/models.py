from django.db import models
from django.conf import settings

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from home.models import BasePage


class EventCategory(models.Model):
    name = models.TextField()
    color_scheme = models.CharField(
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="light-gray",
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('color_scheme'),
    ]


class EventPage(BasePage):
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    thumbnail = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    category = models.ForeignKey(EventCategory, null=True, on_delete=models.SET_NULL)
    start_time = models.TimeField()
    end_time = models.TimeField()

    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
        FieldPanel('long_description'),
        FieldPanel('thumbnail'),
        FieldPanel('category'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
    ]

    parent_page_types = [
        'events.EventListPage'
    ]


class EventListPage(BasePage):
    subpage_types = [
        'events.EventPage',
    ]


class EventListArchivePage(BasePage):
    subpage_types = []


EventPage._meta.get_field('color_scheme').default = 'light-gray'
EventListPage._meta.get_field('color_scheme').default = 'light-gray'
EventListArchivePage._meta.get_field('color_scheme').default = 'light-gray'

