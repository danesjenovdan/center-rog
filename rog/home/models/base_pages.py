from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import NoReverseMatch, reverse
from django.utils import translation as translation

from wagtail import blocks
from wagtail.models import Page, Site
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock

from wagtail.coreutils import (
    WAGTAIL_APPEND_SLASH,
    get_supported_content_language_variant,
)

from .image import CustomImage


class TranslatablePage(Page):
    class Meta:
        abstract = True

    def get_url_parts(self, request=None):
        """
        Determine the URL for this page and return it as a tuple of
        ``(site_id, site_root_url, page_url_relative_to_site_root)``.
        Return None if the page is not routable.

        This is used internally by the ``full_url``, ``url``, ``relative_url``
        and ``get_site`` properties and methods; pages with custom URL routing
        should override this method in order to have those operations return
        the custom URLs.

        Accepts an optional keyword argument ``request``, which may be used
        to avoid repeated database / cache lookups. Typically, a page model
        that overrides ``get_url_parts`` should not need to deal with
        ``request`` directly, and should just pass it to the original method
        when calling ``super``.
        """
        possible_sites = self._get_relevant_site_root_paths(request)

        if not possible_sites:
            return None

        site_id, root_path, root_url, language_code = possible_sites[0]

        site = Site.find_for_request(request)
        if site:
            for site_id, root_path, root_url, language_code in possible_sites:
                if site_id == site.pk:
                    break
            else:
                site_id, root_path, root_url, language_code = possible_sites[0]

        # WORKAROUND for model translation
        language_code = translation.get_language()

        use_wagtail_i18n = getattr(settings, "WAGTAIL_I18N_ENABLED", False)

        if use_wagtail_i18n:
            # If the active language code is a variant of the page's language, then
            # use that instead
            # This is used when LANGUAGES contain more languages than WAGTAIL_CONTENT_LANGUAGES
            try:
                if (
                    get_supported_content_language_variant(translation.get_language())
                    == language_code
                ):
                    language_code = translation.get_language()
            except LookupError:
                # active language code is not a recognised content language, so leave
                # page's language code unchanged
                pass

        # The page may not be routable because wagtail_serve is not registered
        # This may be the case if Wagtail is used headless
        try:
            if use_wagtail_i18n:
                with translation.override(language_code):
                    page_path = reverse(
                        "wagtail_serve", args=(self.url_path[len(root_path) :],)
                    )
            else:
                page_path = reverse(
                    "wagtail_serve", args=(self.url_path[len(root_path) :],)
                )
        except NoReverseMatch:
            return (site_id, None, None)

        # Remove the trailing slash from the URL reverse generates if
        # WAGTAIL_APPEND_SLASH is False and we're not trying to serve
        # the root path
        if not WAGTAIL_APPEND_SLASH and page_path != "/":
            page_path = page_path.rstrip("/")

        return (site_id, root_url, page_path)


class BasePage(TranslatablePage):
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
    image_description = models.TextField(blank=True, verbose_name=_("Dodaten opis slike"), max_length=250)
    # contact information
    email = models.EmailField(blank=True, verbose_name=_("Elektronski naslov"))
    phone = models.CharField(max_length=12, blank=True, verbose_name=_("Telefonska številka"))
    instagram = models.URLField(blank=True, verbose_name=_("Instagram"))
    facebook = models.URLField(blank=True, verbose_name=_("Facebook"))
    website = models.URLField(blank=True, verbose_name=_("Spletna stran"))
    contact_description = models.TextField(blank=True, verbose_name=_("Dodatna informacija"), max_length=50)
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
                FieldPanel("instagram"),
                FieldPanel("facebook"),
                FieldPanel("website"),
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["object_profile_page_type"] = self.__class__.__name__
        return context

    class Meta:
        abstract = True


class BasicTextPage(TranslatablePage):
    body = RichTextField(blank=True, null=True, verbose_name=_("Telo"))

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    subpage_types = []

    class Meta:
        verbose_name = _("Osnovna stran z besedilom")
        verbose_name_plural = _("Osnovne strani z besedilom")
