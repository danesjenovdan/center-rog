from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField

from datetime import date

from home.models import BasePage, CustomImage, Workshop

import random


def add_see_more_fields(context):
    from home.models import LabPage, StudioPage
    from news.models import NewsPage
    # random event
    events = list(EventPage.objects.live())
    context["event"] = random.choice(events) if events else None
    # random news
    news = list(NewsPage.objects.live())
    context["news"] = random.choice(news) if news else None
    # random lab
    labs = list(LabPage.objects.live())
    context["lab"] = random.choice(labs) if labs else None
    # random studio
    studios = list(StudioPage.objects.live().filter(archived=False))
    context["studio"] = random.choice(studios) if studios else None

    return context


class EventCategory(models.Model):
    name = models.TextField(verbose_name=_("Ime kategorije"),)
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
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name=_("Slika dogodka"))
    category = models.ForeignKey(
        EventCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Kategorija"))
    body = RichTextField(blank=True, null=True, verbose_name=_("Telo"))
    tag = models.CharField(max_length=16, blank=True, null=True, verbose_name=_("Oznaka na kartici"))
    start_time = models.TimeField(verbose_name=_("Ura začetka"))
    end_time = models.TimeField(verbose_name=_("Ura konca"))
    start_day = models.DateField(verbose_name=_("Datum začetka"))
    end_day = models.DateField(blank=True, null=True, verbose_name=_("Datum konca (če gre za večdneven dogodek)"))
    location = models.TextField(blank=True, default="Center Rog", verbose_name=_("Lokacija"))
    notice = models.CharField(max_length=45, blank=True, verbose_name=_("Opomba"))
    event_is_workshop = models.ForeignKey(Workshop, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Dogodek je usposabljanje"))
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

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
        FieldPanel("notice"),
        FieldPanel("event_is_workshop"),
        FieldPanel("show_see_more_section")
    ]

    parent_page_types = [
        "events.EventListPage"
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Dogodek")
        verbose_name = _("Dogodki")


class EventListArchivePage(BasePage):
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("show_see_more_section")
    ]

    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        today = date.today()

        context["list"] = EventPage.objects.live().filter(start_day__lt=today).order_by("-start_day")

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv programa")
        verbose_name_plural = _("Arhivi programov")


class EventListPage(BasePage):
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("show_see_more_section")
    ]

    subpage_types = [
        "events.EventPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # categories
        categories = EventCategory.objects.all()
        context["secondary_navigation"] = categories

        today = date.today()

        all_event_page_objects = EventPage.objects.live().filter(start_day__gte=today).order_by("start_day", "start_time")

        # filtering
        chosen_category = categories.filter(slug=request.GET.get('category', None)).first()
        if chosen_category:
            all_event_page_objects = all_event_page_objects.filter(category=chosen_category)

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

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programi")


EventPage._meta.get_field("color_scheme").default = "light-gray"
EventListPage._meta.get_field("color_scheme").default = "light-gray"
EventListArchivePage._meta.get_field("color_scheme").default = "light-gray"
