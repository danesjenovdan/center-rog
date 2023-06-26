from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

from home.models import BasePage, CustomImage


class NewsCategory(models.Model):
    name = models.TextField()
    color_scheme = models.CharField(
        max_length=20,
        choices=settings.COLOR_SCHEMES,
        default="light-gray",
    )

    panels = [
        FieldPanel('category_name'),
        FieldPanel('color_scheme'),
    ]


class NewsPage(BasePage):
    short_description = models.TextField(blank=True)
    thumbnail = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    category = models.ForeignKey(
        NewsCategory, null=True, on_delete=models.SET_NULL)
    hero_image = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    body = RichTextField(blank=True, null=True)
    gallery = StreamField([
        ('image', ImageChooserBlock())
    ], use_json_field=False, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
        FieldPanel('thumbnail'),
        FieldPanel('category'),
        FieldPanel('hero_image'),
        FieldPanel('body'),
        # FieldPanel('gallery'),

    ]

    parent_page_types = [
        'news.NewsListPage'
    ]


class NewsListPage(BasePage):
    subpage_types = [
        'news.NewsPage',
    ]

    def get_context(self, request):
        context = super().get_context(request)
        all_news_page_objects = NewsPage.objects.live().order_by('-first_published_at')
        paginator = Paginator(all_news_page_objects, 6)
        page = request.GET.get("page")
        try:
            news_pages = paginator.page(page)
        except PageNotAnInteger:
            news_pages = paginator.page(1)
        except EmptyPage:
            news_pages = paginator.page(paginator.num_pages)
        context['news_pages'] = news_pages
        return context


class NewsListArchivePage(BasePage):
    subpage_types = []


NewsPage._meta.get_field('color_scheme').default = 'light-gray'
NewsListPage._meta.get_field('color_scheme').default = 'light-gray'
NewsListArchivePage._meta.get_field('color_scheme').default = 'light-gray'
