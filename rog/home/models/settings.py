from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

from wagtail.admin.panels import (
    FieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from .image import CustomImage

import random


## CUSTOM CONTEXT PROCESSORS

def footer_image_processor(request):
    random_image = None

    last_20_images = list(CustomImage.objects.filter(show_in_footer=True)[:20])
    if (last_20_images):
        random_image = random.choice(last_20_images)
    return {'random_image': random_image}

# @register_snippet
# class Infopush(models.Model):
#     tag = models.TextField(null=True, blank=True, verbose_name='Oznaka')
#     title = models.TextField(verbose_name='Naslov (obvezno)')
#     text = models.TextField(verbose_name='Opis')
#     page = models.ForeignKey('wagtailcore.Page', related_name='+', on_delete=models.CASCADE, verbose_name='Povezava do strani (obvezno)')
#     page_text = models.TextField(verbose_name='Besedilo na gumbu (obvezno)')
#     image = models.ForeignKey(
#         "wagtailimages.Image",
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="+",
#     )

#     panels = [
#         FieldPanel('tag'),
#         FieldPanel('title'),
#         FieldPanel('text', classname="full"),
#         FieldPanel('page_text'),
#         FieldPanel('page'),
#         FieldPanel('image')
#     ]

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = "Obvestilo na domači strani"
#         verbose_name_plural = "Obvestila na domači strani"


class ExternalLinkBlock(blocks.StructBlock):
    name = blocks.CharBlock(label="Ime")
    url = blocks.URLBlock(label="URL")
    link_type = blocks.ChoiceBlock(label="Tip povezave", choices=[
        ("button", "Gumb"),
        ("link", "Povezava s puščico")
    ], default="button")

    class Meta:
        label = "Zunanja povezava"
        icon = "link"


class PageLinkBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        required=False,
        label="Ime",
        help_text="Če je prazno, se uporabi naslov strani.",
    )
    page = blocks.PageChooserBlock(label="Stran")
    link_type = blocks.ChoiceBlock(label="Tip povezave", choices=[
        ("button", "Gumb"),
        ("link", "Povezava s puščico")
    ], default="button")

    class Meta:
        label = "Povezava do strani"
        icon = "link"


@register_setting(icon="cog")
class MetaSettings(BaseGenericSetting):
    organization_name = models.TextField(verbose_name=_("Ime"))
    organization_address = models.TextField(verbose_name=_("Ulica in hišna številka"))
    organization_postal_number = models.IntegerField(verbose_name=_("Poštna številka"), validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    organization_post = models.TextField(verbose_name=_("Pošta"))
    organization_country = models.TextField(verbose_name=_("Država"))
    organization_email = models.EmailField(verbose_name=_("E-pošta"))
    organization_phone_number = models.CharField(verbose_name=_("Telefonska številka"), max_length=20)
    organization_working_hours = StreamField([
        ('time', blocks.StructBlock([
            ('day', blocks.CharBlock(label=_('Dan'))),
            ('start_time', blocks.TimeBlock(label=_('Začetna ura'))),
            ('end_time', blocks.TimeBlock(label=_('Končna ura'))),
        ], label=_('Dan in ura')))
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Delovni čas organizacije"))

    basic_information_tab_panels = [
        FieldPanel("organization_name"),
        FieldPanel("organization_address"),
        FieldPanel("organization_postal_number"),
        FieldPanel("organization_post"),
        FieldPanel("organization_country"),
        FieldPanel("organization_email"),
        FieldPanel("organization_phone_number"),
        FieldPanel("organization_working_hours"),
    ]

    social_media_links = StreamField(
        [
            ("external_link", ExternalLinkBlock()),
        ],
        verbose_name="Družbena omrežja",
        use_json_field=True,
        blank=True
    )

    social_media_tab_panels = [
        FieldPanel("social_media_links"),
    ]

    header_marquee = models.TextField(verbose_name=_("Vrteče besedilo"), blank=True, null=True)
    header_links = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
        ],
        verbose_name="Povezave v navigacijski vrstici",
        use_json_field=True,
        blank=True
    )

    header_tab_panels = [
        FieldPanel("header_marquee"),
        FieldPanel("header_links"),
    ]

    footer_links = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
        ],
        verbose_name=_("Povezave v nogi"),
        use_json_field=True,
        blank=True
    )

    footer_images = StreamField(
        [
            ("logo", blocks.StructBlock([
                ("image", ImageChooserBlock()),
                ("description", blocks.CharBlock(label=_("Naslov"), blank=True, required=False))
            ]))
        ],
        block_counts = {
            "logo": {"max_num": 4},
        },
        verbose_name=_("Logotipi"),
        use_json_field=True,
        blank=True
    )

    footer_tab_panels = [
        FieldPanel("footer_links"),
        FieldPanel("footer_images")
    ]

    # meta_image = models.ForeignKey(
    #     "wagtailimages.Image",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    #     verbose_name="OG slika",
    # )

    edit_handler = TabbedInterface(
        [
            ObjectList(basic_information_tab_panels, heading="Osnovne informacije o organizaciji"),
            ObjectList(social_media_tab_panels, heading="Družbena omrežja"),
            ObjectList(header_tab_panels, heading="Navigacija"),
            ObjectList(footer_tab_panels, heading="Noga"),
        ]
    )

    class Meta:
        verbose_name = "Nastavitve spletnega mesta"
