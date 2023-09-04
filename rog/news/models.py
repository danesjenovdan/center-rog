from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

from home.models import BasePage, CustomImage

import random


def add_see_more_fields(context):
    from home.models import LabPage, StudioPage
    from events.models import EventPage
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


class NewsCategory(models.Model):
    name = models.TextField(verbose_name=_("Ime kategorije"))
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
        super(NewsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kategorija novic")
        verbose_name_plural = _("Novice - kategorije")


class NewsPage(BasePage):
    short_description = models.TextField(blank=True, verbose_name=_("Kratek opis"))
    thumbnail = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name=_("Predogledna slika"))
    category = models.ForeignKey(
        NewsCategory, null=True, on_delete=models.SET_NULL, verbose_name=_("Kategorija"))
    hero_image = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name=_("Naslovna slika"))
    body = RichTextField(blank=True, null=True, verbose_name=_("Telo"))
    tag = models.CharField(max_length=16, blank=True, null=True, verbose_name=_("Oznaka"))
    gallery = StreamField([
        ("image", blocks.StructBlock([
            ("image", ImageChooserBlock(label=_("Slika"))),
            ("image_description", blocks.TextBlock(label=_("Podnapis k sliki")))
        ]))
    ], blank=True, null=True, use_json_field=True, verbose_name=_("Galerija"))
    archived = models.BooleanField(default=False, verbose_name=_("Arhiviraj"))
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("short_description"),
        FieldPanel("thumbnail"),
        FieldPanel("category"),
        FieldPanel("hero_image"),
        FieldPanel("body"),
        FieldPanel("tag"),
        FieldPanel("gallery"),
        FieldPanel("archived"),
        FieldPanel("show_see_more_section")
    ]

    parent_page_types = [
        "news.NewsListPage"
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Novica")
        verbose_name_plural = _("Novice")


class NewsListArchivePage(BasePage):
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("show_see_more_section")
    ]

    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["list"] = NewsPage.objects.live().filter(archived=True)

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Arhiv novic")
        verbose_name_plural = _("Arhivi novic")


class NewsListPage(BasePage):
    show_see_more_section = models.BooleanField(default=True, verbose_name=_("Pokaži več"))

    content_panels = Page.content_panels + [
        FieldPanel("show_see_more_section")
    ]

    subpage_types = [
        "news.NewsPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # categories
        categories = NewsCategory.objects.all()
        context["secondary_navigation"] = categories

        all_news_page_objects = NewsPage.objects.live().filter(archived=False).order_by("-first_published_at")

        # filtering
        chosen_category = categories.filter(slug=request.GET.get('category', None)).first()
        if chosen_category:
            all_news_page_objects = all_news_page_objects.filter(category=chosen_category)

        # arhiv
        context["archive_page"] = NewsListArchivePage.objects.live().first()

        # pagination
        paginator = Paginator(all_news_page_objects, 11)
        page = request.GET.get("page")
        try:
            news_pages = paginator.page(page)
        except PageNotAnInteger:
            news_pages = paginator.page(1)
        except EmptyPage:
            news_pages = paginator.page(paginator.num_pages)

        context["news_pages"] = news_pages

        # see more
        context = add_see_more_fields(context)

        return context

    class Meta:
        verbose_name = _("Novice")
        verbose_name_plural = _("Novice")


NewsPage._meta.get_field("color_scheme").default = "light-gray"
NewsListPage._meta.get_field("color_scheme").default = "light-gray"
NewsListArchivePage._meta.get_field("color_scheme").default = "light-gray"
