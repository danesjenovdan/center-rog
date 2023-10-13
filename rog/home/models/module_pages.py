from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField

from .blocks import (ModuleBlock)
from .base_pages import BasePage, TranslatablePage
from .image import CustomImage
from .pages import add_see_more_fields

class HomePage(TranslatablePage):
    body = StreamField(
        ModuleBlock(),
        verbose_name="Telo",
        null=True,
        use_json_field=True
    )

    meta_image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Meta slika")
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('meta_image'),
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
        # 'news.NewsListArchivePage'
    ]


class ContentPage(TranslatablePage):
    secondary_navigation = models.BooleanField(default=False, verbose_name="Sekundarni meni")
    body = StreamField(
        ModuleBlock(),
        verbose_name="Telo",
        use_json_field=True
    )
    show_see_more_section = models.BooleanField(default=False, verbose_name=_("Pokaži več"))

    meta_image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Meta slika")
    )

    content_panels = Page.content_panels + [
        FieldPanel('secondary_navigation'),
        FieldPanel('body'),
        FieldPanel('show_see_more_section')
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('meta_image'),
    ]

    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Generična stran")
        verbose_name_plural = _("Generične strani")
