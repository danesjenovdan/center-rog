from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

from home.models import BasePage


class NewsPage(BasePage):
    short_description = models.TextField(blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    body = RichTextField(blank=True, null=True)
    gallery = StreamField([
        ('image', ImageChooserBlock())
    ], use_json_field=False, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
        FieldPanel('hero_image'),
        FieldPanel('body'),
        FieldPanel('gallery'),

    ]

    parent_page_types = [
        'news.NewsListPage'
    ]


class NewsListPage(BasePage):
    subpage_types = [
        'news.NewsPage',
    ]


class NewsListArchivePage(BasePage):
    subpage_types = []


NewsPage._meta.get_field('color_scheme').default = 'light-gray'
NewsListPage._meta.get_field('color_scheme').default = 'light-gray'
NewsListArchivePage._meta.get_field('color_scheme').default = 'light-gray'
