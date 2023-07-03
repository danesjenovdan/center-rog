from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock

from .image import CustomImage


class BasePage(Page):
    color_scheme = models.CharField(
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="white",
    )

    def short_title(self):
        if len(self.title) > 65:
            return self.title[:62] + "..."
        else:
            return self.title

    class Meta:
        abstract = True


class ObjectListPage(BasePage):
    intro_text = models.TextField(blank=True)
    show_see_more_section = models.BooleanField(default=False, verbose_name=_("Dodaj sekcijo 'Poglej več'"))

    content_panels = Page.content_panels + [
        FieldPanel("intro_text"),
        FieldPanel("show_see_more_section"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    class Meta:
        abstract = True


class ObjectArchiveListPage(BasePage):
    show_see_more_section = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("show_see_more_section"),
    ]

    class Meta:
        abstract = True


class ObjectProfilePage(BasePage):
    description = models.TextField(blank=True, verbose_name=_("Opis"))
    image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Slika")
    )
    image_description = models.TextField(blank=True, verbose_name=_("Dodaten opis slike"))
    # contact information
    email = models.EmailField(blank=True, verbose_name=_("Elektronski naslov"))
    phone = models.CharField(max_length=12, blank=True, verbose_name=_("Telefonska številka"))
    link_1 = models.URLField(blank=True, verbose_name=_("Povezava"))
    link_2 = models.URLField(blank=True, verbose_name=_("Povezava"))
    link_3 = models.URLField(blank=True, verbose_name=_("Povezava"))
    contact_description = models.TextField(blank=True, verbose_name=_("Dodatna informacija"))
    # working hours
    working_hours = StreamField([
        ("time", blocks.StructBlock([
            ("day", blocks.CharBlock(label=_("Dan"))),
            ("start_time", blocks.TimeBlock(label=_("Začetna ura"))),
            ("end_time", blocks.TimeBlock(label=_("Končna ura"))),
        ], label=_("Dan in ura")))
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Delovni čas"))
    # gallery
    gallery = StreamField([
        ("image", ImageChooserBlock(label=_("Slika")))
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Galerija"))
    archived = models.BooleanField(default=False, verbose_name=_("Arhiviraj"))
    show_see_more_section = models.BooleanField(default=False, verbose_name=_("Pokaži več"))
    
    content_panels = Page.content_panels + [
        FieldPanel("description"),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("phone"),
                FieldPanel("link_1"),
                FieldPanel("link_2"),
                FieldPanel("link_3"),
                FieldPanel("contact_description"),
            ],
            heading=_("Kontaktni podatki")
        ),
        FieldPanel("working_hours"),
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("image_description"),
            ],
            heading=_("Slika")
        ),
        FieldPanel("gallery"),
        FieldPanel("archived"),
        FieldPanel("show_see_more_section"),
    ]

    subpage_types = []

    def short_description(self):
        if len(self.description) > 240:
            return self.description[:237] + "..."
        else:
            return self.description

    class Meta:
        abstract = True


class BasicTextPage(Page):
    body = RichTextField(blank=True, null=True, verbose_name=_("Telo"))

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    subpage_types = []

    class Meta:
        verbose_name = _("Osnovna stran z besedilom")
        verbose_name_plural = _("Osnovne strani z besedilom")

