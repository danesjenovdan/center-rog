from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField

from home.models import BasePage, CustomImage


class EventCategory(models.Model):
    name = models.TextField()
    color_scheme = models.CharField(
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="light-gray",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("color_scheme"),
    ]

    class Meta:
        verbose_name = _("Kategorije dogodkov")


class EventPage(BasePage):
    short_description = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    category = models.ForeignKey(
        EventCategory, null=True, blank=True, on_delete=models.SET_NULL)
    body = RichTextField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_day = models.DateField()
    end_day = models.DateField()
    location = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("short_description"),
        FieldPanel("hero_image"),
        FieldPanel("category"),
        FieldPanel("body"),
        FieldPanel("start_day"),
        FieldPanel("end_day"),
        FieldPanel("start_time"),
        FieldPanel("end_time"),
        FieldPanel("location")
    ]

    parent_page_types = [
        "events.EventListPage"
    ]


class EventListPage(BasePage):
    subpage_types = [
        "events.EventPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)
        all_event_page_objects = EventPage.objects.live().order_by("-first_published_at")
        paginator = Paginator(all_event_page_objects, 3)
        page = request.GET.get("page")
        try:
            event_pages = paginator.page(page)
        except PageNotAnInteger:
            event_pages = paginator.page(1)
        except EmptyPage:
            event_pages = paginator.page(paginator.num_pages)
        context["event_pages"] = event_pages
        return context


class EventListArchivePage(BasePage):
    subpage_types = []


EventPage._meta.get_field("color_scheme").default = "light-gray"
EventListPage._meta.get_field("color_scheme").default = "light-gray"
EventListArchivePage._meta.get_field("color_scheme").default = "light-gray"
