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
from wagtail.documents import get_document_model

from .image import CustomImage


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
    link_type = blocks.ChoiceBlock(
        label="Tip povezave",
        choices=[
            ("primary_button", "Primarni gumb"),
            ("secondary_button", "Sekundarni gumb"),
            ("link", "Povezava s puščico"),
        ],
        default="primary_button",
    )

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
    link_type = blocks.ChoiceBlock(
        label="Tip povezave",
        choices=[
            ("primary_button", "Primarni gumb"),
            ("secondary_button", "Sekundarni gumb"),
            ("link", "Povezava s puščico"),
        ],
        default="primary_button",
    )

    class Meta:
        label = "Povezava do strani"
        icon = "link"


@register_setting(icon="cog")
class MetaSettings(BaseGenericSetting):
    organization_name = models.TextField(verbose_name=_("Ime"), blank=True, null=True)
    organization_address = models.TextField(
        verbose_name=_("Ulica in hišna številka"), blank=True, null=True
    )
    organization_postal_number = models.IntegerField(
        verbose_name=_("Poštna številka"),
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        blank=True,
        null=True,
    )
    organization_post = models.TextField(verbose_name=_("Pošta"), blank=True, null=True)
    organization_country = models.TextField(
        verbose_name=_("Država"), blank=True, null=True
    )
    organization_email = models.EmailField(
        verbose_name=_("E-pošta"), blank=True, null=True
    )
    organization_phone_number = models.CharField(
        verbose_name=_("Telefonska številka"), max_length=20, blank=True, null=True
    )
    organization_notice = models.TextField(
        verbose_name=_("Delovni čas info"), blank=True, null=True
    )
    organization_working_hours_title = models.TextField(
        verbose_name=_("Delovni čas organizacije - naslov stolpca"),
        blank=True,
        null=True,
    )
    organization_working_hours = StreamField(
        [
            (
                "time",
                blocks.StructBlock(
                    [
                        ("day", blocks.CharBlock(label=_("Dan"))),
                        ("start_time", blocks.TimeBlock(label=_("Začetna ura"))),
                        ("end_time", blocks.TimeBlock(label=_("Končna ura"))),
                    ],
                    label=_("Dan in ura"),
                ),
            ),
            (
                "notice",
                blocks.StructBlock(
                    [
                        ("day", blocks.CharBlock(label=_("Dan"))),
                        ("text", blocks.CharBlock(label=_("Opomba"))),
                    ],
                    label=_("Dan in opomba"),
                ),
            ),
        ],
        blank=True,
        null=True,
        verbose_name=_("Delovni čas organizacije"),
    )
    labs_working_hours_title = models.TextField(
        verbose_name=_("Delovni čas laboratorijev - naslov stolpca"), blank=True, null=True
    )
    holidays_pdf = models.ForeignKey(
        get_document_model(),
        verbose_name=_("PDF s prazni za trenutno leto"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    labs_working_hours = StreamField(
        [
            (
                "time",
                blocks.StructBlock(
                    [
                        ("day", blocks.CharBlock(label=_("Dan"))),
                        ("start_time", blocks.TimeBlock(label=_("Začetna ura"))),
                        ("end_time", blocks.TimeBlock(label=_("Končna ura"))),
                    ],
                    label=_("Dan in ura"),
                ),
            ),
            (
                "notice",
                blocks.StructBlock(
                    [
                        ("day", blocks.CharBlock(label=_("Dan"))),
                        ("text", blocks.CharBlock(label=_("Opomba"))),
                    ],
                    label=_("Dan in opomba"),
                ),
            ),
        ],
        blank=True,
        null=True,
        verbose_name=_("Delovni čas laboratorijev"),
    )

    basic_information_tab_panels = [
        FieldPanel("organization_name"),
        FieldPanel("organization_address"),
        FieldPanel("organization_postal_number"),
        FieldPanel("organization_post"),
        FieldPanel("organization_country"),
        FieldPanel("organization_email"),
        FieldPanel("organization_phone_number"),
        FieldPanel("organization_notice"),
        FieldPanel("organization_working_hours_title"),
        FieldPanel("organization_working_hours"),
        FieldPanel("labs_working_hours_title"),
        FieldPanel("labs_working_hours"),
        FieldPanel("holidays_pdf"),
    ]

    social_media_links = StreamField(
        [
            ("external_link", ExternalLinkBlock()),
        ],
        verbose_name="Družbena omrežja",
        blank=True,
    )

    social_media_tab_panels = [
        FieldPanel("social_media_links"),
    ]

    header_marquee = models.TextField(
        verbose_name=_("Vrteče besedilo"), blank=True, null=True
    )
    header_links = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
        ],
        verbose_name="Povezave v navigacijski vrstici",
        blank=True,
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
        blank=True,
    )

    footer_logos = StreamField(
        [
            (
                "logo",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock()),
                        (
                            "description",
                            blocks.CharBlock(
                                label=_("Naslov"), blank=True, required=False
                            ),
                        ),
                    ]
                ),
            )
        ],
        block_counts={
            "logo": {"max_num": 4},
        },
        verbose_name=_("Logotipi"),
        blank=True,
    )

    footer_random_images = StreamField(
        [
            (
                "image",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock()),
                    ],
                    label=_("Slika"),
                ),
            )
        ],
        verbose_name=_("Naključne slike v nogi"),
        blank=True,
    )

    newsletter_terms_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    footer_tab_panels = [
        FieldPanel("newsletter_terms_page"),
        FieldPanel("footer_links"),
        FieldPanel("footer_logos"),
        FieldPanel("footer_random_images"),
    ]

    meta_image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Meta slika",
    )

    promotion_tab_panels = [
        FieldPanel("meta_image"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(
                basic_information_tab_panels,
                heading="Osnovne informacije o organizaciji",
            ),
            ObjectList(social_media_tab_panels, heading="Družbena omrežja"),
            ObjectList(header_tab_panels, heading="Navigacija"),
            ObjectList(footer_tab_panels, heading="Noga"),
            ObjectList(promotion_tab_panels, heading="Promocija"),
        ]
    )

    class Meta:
        verbose_name = "Nastavitve spletnega mesta"
