from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
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


class BasePage(Page):
    COLOR_SCHEMES = [
        ("brown", "Rjava"),
        ("light-gray", "Svetlo siva"),
        ("dark-gray", "Temno siva"),
        ("light-blue", "Svetlo modra"),
        ("dark-blue", "Temno modra"),
        ("light-green", "Svetlo zelena"),
        ("dark-green", "Temno zelena"),
        ("purple", "Vijolična"),
        ("red", "Rdeča"),
        ("orange", "Oranžna"),
        ("pink", "Roza"),
        ("yellow", "Rumena"),
        ("white", "Bela"),
    ]
    
    color_scheme = models.CharField(
        max_length=20,
        choices=COLOR_SCHEMES,
        default="white",
    )

    class Meta:
        abstract = True


class ObjectListPage(BasePage):
    intro_text = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
    ]


class ObjectProfilePage(BasePage):
    description = models.TextField(blank=True)
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

    content_panels = Page.content_panels + [
        FieldPanel('description'),
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


class StudioPage(ObjectProfilePage):
    pass

StudioPage._meta.get_field('color_scheme').default = 'yellow'


class ResidencePage(ObjectProfilePage):
    pass

ResidencePage._meta.get_field('color_scheme').default = 'dark-gray'


class MarketStorePage(ObjectProfilePage):
    pass

MarketStorePage._meta.get_field('color_scheme').default = 'brown'


class LibraryPage(ObjectProfilePage):
    pass

LibraryPage._meta.get_field('color_scheme').default = 'pink'


class ContentPage(Page):
    pass
    # content_panels = Page.content_panels + [
    #     FieldPanel('color_scheme'),
    # ]
    