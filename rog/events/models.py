from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField

from home.models import BasePage, CustomImage, Workshop


class EventCategory(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    color_scheme = models.CharField(
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
        verbose_name_plural = _("Kategorije dogodkov")


class EventPage(BasePage):
    hero_image = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name=_("Slika dogodka"))
    category = models.ForeignKey(
        EventCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Kategorija"))
    body = RichTextField(blank=True, null=True, verbose_name=_("Telo"))
    tag = models.CharField(max_length=16, blank=True, null=True, verbose_name=_("Oznaka"))
    start_time = models.TimeField(verbose_name=_("Ura začetka"))
    end_time = models.TimeField(verbose_name=_("Ura konca"))
    start_day = models.DateField(verbose_name=_("Datum začetka"))
    end_day = models.DateField(blank=True, null=True, verbose_name=_("Datum konca (če gre za večdneven dogodek)"))
    location = models.TextField(blank=True, default="Center Rog", verbose_name=_("Lokacija"))
    event_is_workshop = models.ForeignKey(Workshop, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Dogodek je usposabljanje"))
    archived = models.BooleanField(default=False, verbose_name=_("Arhiviraj"))
    show_see_more_section = models.BooleanField(default=False, verbose_name=_("Pokaži več"))

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
        FieldPanel("event_is_workshop"),
        FieldPanel("archived"),
        FieldPanel("show_see_more_section")
    ]

    parent_page_types = [
        "events.EventListPage"
    ]

    class Meta:
        verbose_name = _("Dogodek")
        verbose_name = _("Dogodki")


class EventListArchivePage(BasePage):
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["list"] = EventPage.objects.live().filter(archived=True)

        # see more
        # context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv dogodkov")
        verbose_name_plural = _("Arhivi dogodkov")


class EventListPage(BasePage):
    subpage_types = [
        "events.EventPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # categories
        categories = EventCategory.objects.all()
        context["secondary_navigation"] = categories

        all_event_page_objects = EventPage.objects.live().filter(archived=False).order_by("-first_published_at")

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

        return context

    class Meta:
        verbose_name = _("Seznam dogodkov")
        verbose_name_plural = _("Seznami dogodkov")


EventPage._meta.get_field("color_scheme").default = "light-gray"
EventListPage._meta.get_field("color_scheme").default = "light-gray"
EventListArchivePage._meta.get_field("color_scheme").default = "light-gray"
