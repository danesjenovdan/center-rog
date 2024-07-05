from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.edit_handlers import MediaChooserPanel
from modelcluster.fields import ParentalKey

from .base_pages import BasePage, ObjectProfilePage, ObjectListPage, ObjectArchiveListPage
from .image import CustomImage
from .workshop import Workshop
from news.models import NewsPage
from events.models import EventPage

import random
from datetime import date, datetime


def add_see_more_fields(context):
    # random event
    today = date.today()
    events = list(EventPage.objects.live().filter(start_day__gt=today).order_by("start_day"))[:5]
    context["event"] = random.choice(events) if events else None
    # random news
    news = list(NewsPage.objects.live().order_by("-first_published_at"))[:5]
    context["news"] = random.choice(news) if news else None
    # random lab
    labs = list(LabPage.objects.live())
    context["lab"] = random.choice(labs) if labs else None
    # random studio
    studios = list(StudioPage.objects.live().filter(archived=False))
    context["studio"] = random.choice(studios) if studios else None

    return context


def add_see_more_lab_events(context):
    if context["object_profile_page_type"] == "LabPage":
        page = context["page"]
    elif context["object_profile_page_type"] == "WorkingStationPage":
        page = context["page"].get_parent()
    else:
        return context

    # 3 random events from this lab
    today = date.today()
    events = list(
        EventPage.objects.live()
        .filter(labs=page, start_day__gte=today, event_is_workshop__isnull=False)
        .order_by("start_day")
    )
    context["events"] = random.sample(events, min(3, len(events)))

    return context

### OBJECT PROFILE PAGES ###

class StudioPage(ObjectProfilePage):
    thumbnail = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Predogledna slika")
    )

    content_panels = ObjectProfilePage.content_panels + [
        FieldPanel("thumbnail"),
    ]

    parent_page_types = [
        "home.StudioListPage"
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Studio")
        verbose_name_plural = _("Studii")

StudioPage._meta.get_field("color_scheme").default = "yellow"


class ResidencePage(ObjectProfilePage):
    parent_page_types = [
        "home.ResidenceListPage"
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Rezident")
        verbose_name_plural = _("Rezidenti")

ResidencePage._meta.get_field("color_scheme").default = "dark-gray"


class MarketStorePage(ObjectProfilePage):
    card_color_scheme = models.CharField(
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="white",
        verbose_name=_("Barvna shema kartice na seznamu")
    )

    parent_page_types = [
        "home.MarketStoreListPage"
    ]

    content_panels = ObjectProfilePage.content_panels + [
        FieldPanel("card_color_scheme"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Trgovina")
        verbose_name_plural = _("Trgovine")

MarketStorePage._meta.get_field("color_scheme").default = "brown"


class LabPage(BasePage):
    description = models.TextField(blank=True, verbose_name=_("Opis"))
    image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Slika")
    )
    thumbnail = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Predogledna slika")
    )
    gallery = StreamField([
        ("image", blocks.StructBlock([
            ("image", ImageChooserBlock(label=_("Slika"))),
            ("image_description", blocks.TextBlock(label=_("Podnapis k sliki"), max_length=150, required=False))
        ]))
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Galerija"))
    lab_lead = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Vodja laboratorija")
    )
    lab_lead_email = models.EmailField(
        blank=True,
        verbose_name=_("E-mail vodje laboratorija")
    )
    training_dates_link = models.URLField(blank=True, verbose_name=_("Termini usposabljanj"))
    online_trainings_link = models.URLField(blank=True, verbose_name=_("Spletna usposabljanja"))
    optional_button = models.URLField(blank=True, verbose_name=_("Spletna usposabljanja"))
    working_hours = StreamField(
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
            )
        ],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name=_("Delovni čas"),
    )
    notice = models.CharField(
        max_length=50, blank=True, verbose_name=_("Dodatno obvestilo")
    )
    button = StreamField([
        ("external", blocks.URLBlock(label=_("Zunanji URL"))),
        ("page", blocks.PageChooserBlock(label=_("Podstran"))),
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Gumb"), max_num=1)
    button_text = models.TextField(verbose_name=_("Besedilo na gumbu"), blank=True, null=True)
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("thumbnail"),
        FieldPanel("gallery"),
        FieldPanel("lab_lead"),
        FieldPanel("lab_lead_email"),
        FieldPanel("training_dates_link"),
        FieldPanel("online_trainings_link"),
        FieldPanel("working_hours"),
        FieldPanel("notice"),
        FieldPanel("button"),
        FieldPanel("button_text"),
        InlinePanel("related_tools", label="Orodja"),
        FieldPanel("show_see_more_section"),
    ]

    parent_page_types = [
        "home.LabListPage"
    ]

    subpage_types = [
        "home.WorkingStationPage"
    ]

    def short_description(self):
        if len(self.description) > 240:
            return self.description[:237] + "..."
        else:
            return self.description

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["object_profile_page_type"] = self.__class__.__name__

        # see more
        context = add_see_more_lab_events(context)

        # working station pages
        working_stations = WorkingStationPage.objects.live().descendant_of(self)
        context["working_stations"] = working_stations

        return context

    class Meta:
        verbose_name = _("Laboratorij")
        verbose_name_plural = _("Laboratoriji")

LabPage._meta.get_field("color_scheme").default = "light-green"


class WorkingStationPage(BasePage):
    thumbnail = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Predogledna slika"),
    )
    description = models.TextField(blank=True, verbose_name=_("Kratek opis na kartici"))
    image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Slika"),
    )
    modules = StreamField(
        [
            (
                "bulletpoints",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.TextBlock(
                                label=_("Naslov"),
                                required=False,
                            ),
                        ),
                        (
                            "points",
                            blocks.ListBlock(blocks.TextBlock(), label=_("Točka"), min=1),
                        ),
                    ],
                    label=_("Modul s točkami"),
                ),
            ),
            (
                "description",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.TextBlock(
                                label=_("Naslov"),
                                required=False,
                            ),
                        ),
                        (
                            "description",
                            blocks.TextBlock(
                                label=_("Opis"),
                            ),
                        ),
                    ],
                    label=_("Modul z opisom"),
                ),
            ),
            (
                "specifications",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.TextBlock(
                                label=_("Naslov"),
                                required=False,
                            ),
                        ),
                        (
                            "points",
                            blocks.ListBlock(blocks.StructBlock([
                                ("name", blocks.TextBlock(label=_("Specifikacija"))),
                                ("value", blocks.TextBlock(label=_("Vrednost"))),
                            ]), label=_("Specifikacije"), min=1),
                        ),
                    ],
                    label=_("Modul s specifikacijami"),
                ),
            ),
        ],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name=_("Moduli"),
    )
    required_workshop = models.ForeignKey(
        Workshop,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Zahteva usposabljanje?"),
    )
    tag = models.CharField(
        max_length=12, blank=True, null=True, verbose_name=_("Oznaka na kartici")
    )
    prima_location_id = models.IntegerField(
        null=True, blank=True, verbose_name=_("Prima location id")
    )
    prima_group_id = models.IntegerField(
        null=True, blank=True, verbose_name=_("Prima group id")
    )
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("thumbnail"),
        FieldPanel("image"),
        FieldPanel("modules"),
        FieldPanel("required_workshop"),
        FieldPanel("tag"),
        FieldPanel("prima_location_id"),
        FieldPanel("prima_group_id"),
        FieldPanel("show_see_more_section"),
    ]

    parent_page_types = ["home.LabPage"]

    def workshop_event(self):
        today = datetime.today()
        events = EventPage.objects.filter(
            event_is_workshop=self.required_workshop, start_day__gte=today
        ).order_by("start_day")
        if len(events) > 0:
            return events.first()
        else:
            return None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["object_profile_page_type"] = self.__class__.__name__

        # see more
        context = add_see_more_lab_events(context)

        return context

    class Meta:
        verbose_name = _("Delovna postaja")
        verbose_name_plural = _("Delovne postaje")


WorkingStationPage._meta.get_field("color_scheme").default = "light-green"


class LibraryPage(ObjectProfilePage):

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Knjižnica")
        verbose_name_plural = _("Knjižnice")

LibraryPage._meta.get_field("color_scheme").default = "pink"


## OBJECT ARCHIVE LIST PAGES

class StudioArchiveListPage(ObjectArchiveListPage):
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["list"] = StudioPage.objects.live().filter(
            Q(archived=True) | Q(active_to__lt=date.today())
        )

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv studiev")
        verbose_name_plural = _("Arhivi studiev")

StudioArchiveListPage._meta.get_field("color_scheme").default = "yellow"


class ResidenceArchiveListPage(ObjectArchiveListPage):
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["list"] = ResidencePage.objects.live().filter(
            Q(archived=True) | Q(active_to__lt=date.today())
        )

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv rezidentov")
        verbose_name_plural = _("Arhivi rezidentov")

ResidenceArchiveListPage._meta.get_field("color_scheme").default = "dark-gray"


### OBJECT LIST PAGES ###

class StudioListPage(ObjectListPage):
    subpage_types = [
        "home.StudioPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["studios"] = (
            StudioPage.objects.child_of(self)
            .live()
            .filter(
                Q(archived=False) &
                (Q(active_to=None) | Q(active_to__gte=datetime.today())),
            )
        )
        context["archive_page"] = StudioArchiveListPage.objects.live().first()

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Studii")
        verbose_name_plural = _("Studii")

StudioListPage._meta.get_field("color_scheme").default = "yellow"


class MarketStoreListPage(ObjectListPage):
    subpage_types = [
        "home.MarketStorePage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["markets"] = MarketStorePage.objects.child_of(self).live().filter(
                Q(archived=False) &
                (Q(active_to=None) | Q(active_to__gte=datetime.today())),
            )

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Market")
        verbose_name_plural = _("Market")

MarketStoreListPage._meta.get_field("color_scheme").default = "brown"


class ResidenceListPage(ObjectListPage):
    subpage_types = [
        "home.ResidencePage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["residents"] = (
            ResidencePage.objects.child_of(self)
            .live()
            .filter(
                Q(archived=False)
                & (Q(active_to=None) | Q(active_to__gte=datetime.today())),
            )
        )
        context["archive_page"] = ResidenceArchiveListPage.objects.live().first()

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Rezidenti")
        verbose_name_plural = _("Rezidenti")

ResidenceListPage._meta.get_field("color_scheme").default = "dark-gray"


class LabListPage(ObjectListPage):
    subpage_types = [
        "home.LabPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["labs"] = LabPage.objects.child_of(self).live()

       # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Laboratoriji")
        verbose_name_plural = _("Laboratoriji")

LabListPage._meta.get_field("color_scheme").default = "light-green"
