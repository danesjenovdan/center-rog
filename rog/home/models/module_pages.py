from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField

from .blocks import (ModuleBlock)
from .base_pages import BasePage, TranslatablePage

class HomePage(TranslatablePage):
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
        'home.StudioArchiveListPage',
        'home.MarketStoreListPage',
        'home.ResidenceListPage',
        'home.ResidenceArchiveListPage',
        'home.LabListPage',
        'home.LibraryPage',
        'home.BasicTextPage',
        'home.ContentPage',
        'events.EventListPage',
        'events.EventListArchivePage',
        'news.NewsListPage',
        'news.NewsListArchivePage'
    ]

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)

    #     context['exposed_news'] = NewsPage.objects.all().first()
    #     return context



class ContentPage(TranslatablePage):
    secondary_navigation = models.BooleanField(default=False, verbose_name="Sekundarni meni")
    body = StreamField(
        ModuleBlock(),
        verbose_name="Telo",
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('secondary_navigation'),
        FieldPanel('body'),
    ]

    subpage_types = []

    class Meta:
        verbose_name = _("Osnovna stran z moduli")
        verbose_name_plural = _("Osnovne strani z moduli")
