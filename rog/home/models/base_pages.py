from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


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
    show_see_more_section = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
        FieldPanel('show_see_more_section'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    class Meta:
        abstract = True


class ObjectProfilePage(BasePage):
    description = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    # contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    link_1 = models.URLField(blank=True)
    link_2 = models.URLField(blank=True)
    link_3 = models.URLField(blank=True)
    contact_description = models.TextField(blank=True)
    # working hours
    working_hours = StreamField([
        ('time', blocks.StructBlock([
            ('day', blocks.CharBlock(label=_('Dan'))),
            ('start_time', blocks.TimeBlock(label=_('Začetna ura'))),
            ('end_time', blocks.TimeBlock(label=_('Končna ura'))),
        ], label=_('Dan in ura')))
    ], blank=True, null=True, use_json_field=False)
    # gallery
    # gallery = StreamField(
    #     blocks.ListBlock(ImageChooserBlock()),
    #     blank=True,
    #     null=True,
    #     use_json_field=False
    # )
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('image'),
        MultiFieldPanel(
            [
                FieldPanel('email'),
                FieldPanel('phone'),
                FieldPanel('link_1'),
                FieldPanel('link_2'),
                FieldPanel('link_3'),
                FieldPanel('contact_description'),
            ],
            heading=_('Kontaktni podatki')
        ),
        FieldPanel('working_hours'),
    ]

    subpage_types = []

    class Meta:
        abstract = True
