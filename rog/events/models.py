from django.db import models
from django import forms
from django.db.models import Q, F, Count, BooleanField, Case, Value, When
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from wagtail.models import Page, Orderable, PageManager
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

from wagtailautocomplete.edit_handlers import AutocompletePanel

from datetime import date

from home.models import BasePage, CustomImage, Workshop
from payments.pantheon import create_ident

from behaviours.models import Timestampable

import sentry_sdk

import random


def add_see_more_fields(context):
    from home.models import LabPage, StudioPage
    from news.models import NewsPage

    # random event
    today = date.today()
    events = list(
        EventPage.objects.live().filter(start_day__gt=today).order_by("start_day")[:5]
    )
    context["event"] = random.choice(events) if events else None
    # random news
    news = list(NewsPage.objects.live().order_by("-first_published_at")[:5])
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
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_("Opis"),
        help_text=_("Opis kategorije, ki se pojavi nad seznamom dogodkov"),
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
        FieldPanel("description"),
        FieldPanel("color_scheme"),
    ]

    pantheon_ident = models.CharField(
        max_length=16, blank=True, null=True, verbose_name=_("Pantheon ident id")
    )
    saved_in_pantheon = models.BooleanField(
        default=False,
        help_text=_(
            "Ali event category že shranjen v Pantheon ali preprečite shranjevanje v Pantheon"
        ),
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.saved_in_pantheon:
            ident_name = f'{self.name.upper().replace(" ", "")}'[:16]
            self.pantheon_ident = ident_name
            super(EventCategory, self).save(*args, **kwargs)
            try:
                response = create_ident(self.name, float(50), 0, self.pantheon_ident)
                if response and response.status_code == 200:
                    self.saved_in_pantheon = True
                    super(EventCategory, self).save(*args, **kwargs)
                else:
                    if response:
                        sentry_sdk.capture_message(
                            f"Error creating event ident {self.title} on pantheon with response {response.content}"
                        )
            except Exception as e:
                sentry_sdk.capture_exception(e)

        super(EventCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kategorija dogodkov")
        verbose_name_plural = _("Dogodki - kategorije")


class EventPageManager(PageManager):
    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = (
            queryset.annotate(
                booked_users=Count(
                    "event_registrations",
                    filter=Q(
                        event_registrations__registration_finished=True,
                        event_registrations__event_registration_children__isnull=True,
                    ),
                ),
                booked_children=Count(
                    "event_registrations__event_registration_children",
                    filter=Q(event_registrations__registration_finished=True),
                ),
                booked_extra_people=Count(
                    "event_registrations__event_registration_extra_people",
                    filter=Q(event_registrations__registration_finished=True),
                ),
            )
            .annotate(
                booked_count=F("booked_users")
                + F("booked_children")
                + F("booked_extra_people")
            )
            .annotate(free_places=F("number_of_places") - F("booked_count"))
            .annotate(
                has_free_place=Case(
                    When(number_of_places=0, then=Value(True)),
                    When(free_places__gt=0, then=Value(True)),
                    When(free_places__lte=0, then=Value(False)),
                    default_value=Value(False),
                    output_field=BooleanField(),
                )
            )
        )

        return queryset


class EventPage(BasePage):
    hero_image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Slika dogodka"),
    )
    categories = ParentalManyToManyField(
        EventCategory,
        blank=True,
        related_name="event_pages",
        verbose_name=_("Kategorije"),
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
    labs = ParentalManyToManyField(
        "home.LabPage", blank=True, verbose_name=_("Laboratoriji")
    )
    without_registrations = models.BooleanField(
        default=False,
        verbose_name=_("Brez prijave"),
        help_text=_("Če je označeno, je dogodek brez prijave."),
    )
    event_is_for_children = models.BooleanField(
        default=False,
        verbose_name=_("Dogodek je za otroke"),
        help_text=_("Prijava na dogodek zahteva vpis vsaj enega otroka"),
    )
    allowed_extra_people = models.BooleanField(
        default=False,
        verbose_name=_("Dovoljena prijava dodatnih oseb"),
        help_text=_("Pri prijavi na dogodek ja omogoča prijavo dodatnih oseb"),
    )
    just_for_members = models.BooleanField(
        default=False,
        verbose_name=_("Dogodek samo za člane"),
        help_text=_("Za prijavo na dogodek mora biti uporabnik član"),
    )
    required_plan = models.ForeignKey(
        "payments.Plan",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Zahtevan plan"),
        help_text=_("Za prijavo na dogodek mora uporabnik imeti aktiven ta plan"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("categories"),
        FieldPanel("body"),
        FieldPanel("tag"),
        FieldPanel("event_is_for_children"),
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
        FieldPanel("labs", widget=forms.CheckboxSelectMultiple),
        FieldPanel("without_registrations"),
        FieldPanel("allowed_extra_people"),
        FieldPanel("just_for_members"),
        FieldPanel("required_plan"),
    ]

    parent_page_types = ["events.EventListPage"]

    objects = EventPageManager()

    def can_register(self, user):
        if self.just_for_members:
            if not user.is_authenticated:
                return False
            else:
                if not user.membership:
                    return False
        if self.required_plan:
            if not user.has_active_plan(self.required_plan):
                return False

        return True

    def get_free_places(self):
        if getattr(self, "free_places", None) is None:
            # don't calculate free places when event page not saved yet
            return -1
        return self.free_places

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # see more
        context = add_see_more_fields(context)

        context["free_places"] = self.get_free_places()

        current_user = request.user
        if current_user.is_authenticated:
            current_user_registered = EventRegistration.objects.filter(
                event_id=self.id, user=current_user, registration_finished=True
            ).count()
        else:
            current_user_registered = False

        context["current_user_registered"] = current_user_registered

        return context

    @property
    def show_start_day(self):
        today = date.today()
        return self.start_day > today

    def get_admin_display_title(self):
        title = super().get_admin_display_title()
        if not self.start_day:
            return title

        formatted_date = self.start_day.strftime("%d. %m. %Y")
        return f"{title} • [{formatted_date}]"

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

        context["list"] = (
            EventPage.objects.live()
            .filter(start_day__lt=today, end_day__lt=today)
            .order_by("-start_day")
            .prefetch_related("categories")
        )

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

        all_event_page_objects = (
            EventPage.objects.live()
            .filter(Q(start_day__gte=today) | Q(end_day__gte=today))
            .select_related("hero_image")
            .prefetch_related("categories")
            .order_by("-has_free_place", "start_day", "start_time", "id")
        )

        # filtering
        chosen_category = categories.filter(
            slug=request.GET.get("category", None)
        ).first()
        if chosen_category:
            all_event_page_objects = all_event_page_objects.filter(
                categories=chosen_category
            )

        # labs filter
        from home.models import LabPage

        all_lab_ids = list(
            EventPage.objects.live()
            .filter(labs__isnull=False)
            .order_by("labs")
            .values_list("labs", flat=True)
            .distinct()
        )
        all_labs = LabPage.objects.filter(id__in=all_lab_ids).order_by("title")

        lab_slugs = list(filter(bool, map(str.strip, request.GET.get("labs", "").split(","))))
        chosen_labs = all_labs.filter(slug__in=lab_slugs)
        if chosen_labs:
            all_event_page_objects = all_event_page_objects.filter(labs__in=chosen_labs)

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

        # add variables to context
        context["event_pages"] = event_pages
        context["chosen_category"] = chosen_category
        context["all_labs"] = all_labs
        context["chosen_labs"] = chosen_labs

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programi")


# prijavnica (povezava med uporabnikom in dogodkom)
class EventRegistration(Orderable, ClusterableModel, Timestampable):
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
    register_child_check = models.BooleanField(
        verbose_name=_("Na dogodek prijavljam otroka"), default=False
    )
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

    def number_of_people(self):
        # if we have children registered, we count only them
        num_children = self.event_registration_children.count()
        if num_children:
            return num_children

        # otherwise, we count the user and extra people
        num_extra_people = self.event_registration_extra_people.count()
        return 1 + num_extra_people

    panels = [
        AutocompletePanel("user", target_model="users.User"),
        FieldPanel("event"),
        FieldPanel("name"),
        FieldPanel("surname"),
        # FieldPanel("register_child_check"),
        FieldPanel("phone"),
        FieldPanel("disabilities"),
        FieldPanel("allergies"),
        FieldPanel("agreement_responsibility"),
        FieldPanel("allow_photos"),
        FieldPanel("registration_finished"),
        InlinePanel("event_registration_children", label=_("Prijavljeni otroci")),
        InlinePanel("event_registration_extra_people", label=_("Dodatne osebe")),
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


# prijavnica za dodatno osebo (se veže na prijavnico)
class EventRegistrationExtraPerson(Orderable):
    event_registration = ParentalKey(
        EventRegistration,
        on_delete=models.CASCADE,
        related_name="event_registration_extra_people",
    )
    person_name = models.TextField(verbose_name=_("Ime osebe"))
    person_surname = models.TextField(verbose_name=_("Priimek osebe"))


EventPage._meta.get_field("color_scheme").default = "light-gray"
EventListPage._meta.get_field("color_scheme").default = "light-gray"
EventListArchivePage._meta.get_field("color_scheme").default = "light-gray"
