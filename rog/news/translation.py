from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import NewsCategory, NewsListPage, NewsPage


@register(NewsListPage)
class NewsListPageTR(TranslationOptions):
    pass


@register(NewsPage)
class NewsPageTR(TranslationOptions):
    fields = ("short_description", "body")


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
