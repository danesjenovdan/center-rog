from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from datetime import date

from home.models import BasePage, CustomImage, Workshop

import random


def add_see_more_fields(context):
    from home.models import LabPage, StudioPage
    from news.models import NewsPage

    # random event
    today = date.today()
    events = list(
        EventPage.objects.live().filter(start_day__gt=today).order_by("start_day")
    )[:5]
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


class EventCategory(models.Model):
    name = models.TextField(
        verbose_name=_("Ime kategorije"),
    )
    slug = models.SlugField()
    color_scheme = models.CharField(
        verbose_name=_("Barvna shema"),
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="light-gray",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("color_scheme"),
    ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(EventCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kategorija dogodkov")
        verbose_name_plural = _("Dogodki - kategorije")


class EventPage(BasePage):
    hero_image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Slika dogodka"),
    )
    category = models.ForeignKey(
        EventCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Kategorija"),
    )
    body = RichTextField(blank=True, null=True, verbose_name=_("Telo"))
    tag = models.CharField(
        max_length=16, blank=True, null=True, verbose_name=_("Oznaka na kartici")
    )
    start_time = models.TimeField(verbose_name=_("Ura začetka"))
    end_time = models.TimeField(verbose_name=_("Ura konca"))
    start_day = models.DateField(verbose_name=_("Datum začetka"))
    end_day = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Datum konca (če gre za večdneven dogodek)"),
    )
    location = models.TextField(
        blank=True, default="Center Rog", verbose_name=_("Lokacija")
    )
    apply_url = models.URLField(
        blank=True, verbose_name=_("Povezava za prijavo (če je prazno, se gumb skrije)")
    )
    notice = models.CharField(max_length=45, blank=True, verbose_name=_("Opomba"))
    event_is_workshop = models.ForeignKey(
        Workshop,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Dogodek je usposabljanje"),
    )
    show_see_more_section = models.BooleanField(
        default=True, verbose_name=_("Pokaži več")
    )

    price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name=_("Cena")
    )
    price_for_non_member = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name=_("Cena za nečlane")
    )
    number_of_places = models.IntegerField(verbose_name=_("Število mest"), default=0)
    contact_email = models.EmailField(
        verbose_name=_("Kontaktni email"), null=True, blank=True
    )
    labs = models.ManyToManyField(
        "home.LabPage", blank=True, verbose_name=_("Laboratorij")
    )
    without_registrations = models.BooleanField(
        default=False,
        verbose_name=_("Brez prijave"),
        help_text=_("Če je označeno, je dogodek brez prijave."),
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("category"),
        FieldPanel("body"),
        FieldPanel("tag"),
        FieldPanel("start_day"),
        FieldPanel("end_day"),
        FieldPanel("start_time"),
        FieldPanel("end_time"),
        FieldPanel("location"),
        FieldPanel("apply_url"),
        FieldPanel("notice"),
        FieldPanel("event_is_workshop"),
        FieldPanel("show_see_more_section"),
        FieldPanel("price"),
        FieldPanel("price_for_non_member"),
        FieldPanel("number_of_places"),
        FieldPanel("contact_email"),
        FieldPanel("labs"),
        FieldPanel("without_registrations"),
    ]

    parent_page_types = ["events.EventListPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # see more
        context = add_see_more_fields(context)

        free_places = (
            self.number_of_places
            - EventRegistration.objects.filter(
                event=self, registration_finished=True
            ).count()
        )
        context["free_places"] = free_places

        current_user = request.user
        if current_user.is_authenticated:
            current_user_registered = EventRegistration.objects.filter(
                event=self, user=current_user, registration_finished=True
            ).count()
        else:
            current_user_registered = False

        context["current_user_registered"] = current_user_registered

        return context

    class Meta:
        verbose_name = _("Dogodek")
        verbose_name = _("Dogodki")


class EventListArchivePage(BasePage):
    show_see_more_section = models.BooleanField(
        default=True, verbose_name=_("Pokaži več")
    )

    content_panels = Page.content_panels + [FieldPanel("show_see_more_section")]

    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        today = date.today()

        context["list"] = EventPage.objects.live().filter(start_day__lt=today, end_day__lt=today).order_by("-start_day")

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv programa")
        verbose_name_plural = _("Arhivi programov")


class EventListPage(BasePage):
    show_see_more_section = models.BooleanField(
        default=True, verbose_name=_("Pokaži več")
    )

    content_panels = Page.content_panels + [FieldPanel("show_see_more_section")]

    subpage_types = [
        "events.EventPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # categories
        categories = EventCategory.objects.all()
        context["secondary_navigation"] = categories

        today = date.today()

        all_event_page_objects = EventPage.objects.live().filter(Q(start_day__gte=today) | Q(end_day__gte=today)).order_by("start_day", "start_time")

        # filtering
        chosen_category = categories.filter(
            slug=request.GET.get("category", None)
        ).first()
        if chosen_category:
            all_event_page_objects = all_event_page_objects.filter(
                category=chosen_category
            )

        # arhiv
        context["archive_page"] = EventListArchivePage.objects.live().first()

        # pagination
        paginator = Paginator(all_event_page_objects, 11)
        page = request.GET.get("page")
        try:
            event_pages = paginator.page(page)
        except PageNotAnInteger:
            event_pages = paginator.page(1)
        except EmptyPage:
            event_pages = paginator.page(paginator.num_pages)

        context["event_pages"] = event_pages
        context["chosen_category"] = chosen_category

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programi")


# prijavnica (povezava med uporabnikom in dogodkom)
class EventRegistration(Orderable, ClusterableModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )
    event = models.ForeignKey(
        EventPage,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )
    name = models.TextField(verbose_name=_("Ime"), blank=True)
    surname = models.TextField(verbose_name=_("Priimek"), blank=True)
    phone = models.TextField(verbose_name=_("Telefonska številka"), blank=True)
    disabilities = models.TextField(verbose_name=_("Oviranosti (naštej)"), blank=True)
    allergies = models.TextField(verbose_name=_("Alergije (naštej)"), blank=True)
    agreement_responsibility = models.BooleanField(
        verbose_name=_("Strinjam se z zavrnitvijo odgovornosti"), default=False
    )
    allow_photos = models.BooleanField(
        verbose_name=_("Dovoljujem fotografiranje in snemanje"),
        default=False,
    )
    registration_finished = models.BooleanField(
        verbose_name=_("Prijava na dogodek je zaključena"), default=False
    )

    def __str__(self):
        return f"{self.event.title} [{self.user}]"

    panels = [
        FieldPanel("event"),
        FieldPanel("name"),
        FieldPanel("surname"),
        FieldPanel("phone"),
        FieldPanel("disabilities"),
        FieldPanel("allergies"),
        FieldPanel("agreement_responsibility"),
        FieldPanel("allow_photos"),
        FieldPanel("registration_finished"),
        InlinePanel("event_registration_children", label=_("Prijavljeni otroci")),
    ]

    class Meta:
        unique_together = (
            "user",
            "event",
        )
        verbose_name = _("Prijava na dogodek")
        verbose_name_plural = _("Dogodki - prijave")


# prijavnica za otroka (se veže na prijavnico)
class EventRegistrationChild(Orderable):
    event_registration = ParentalKey(
        EventRegistration,
        on_delete=models.CASCADE,
        related_name="event_registration_children",
    )
    child_name = models.TextField(verbose_name=_("Ime otroka"))
    child_surname = models.TextField(verbose_name=_("Priimek otroka"))
    parent_phone = models.TextField(
        verbose_name=_("Telefonska številka zakonitega skrbnika")
    )
    birth_date = models.DateField(verbose_name="Datum rojstva")
    gender = models.CharField(
        max_length=1,
        choices=(("F", "ženski"), ("M", "moški"), ("O", "drugo")),
        verbose_name="Spol",
    )
    gender_other = models.CharField(
        max_length=200, blank=True, verbose_name="Spol (drugo)"
    )


EventPage._meta.get_field("color_scheme").default = "light-gray"
EventListPage._meta.get_field("color_scheme").default = "light-gray"
EventListArchivePage._meta.get_field("color_scheme").default = "light-gray"
