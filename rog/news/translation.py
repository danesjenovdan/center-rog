from .models import NewsListPage, NewsPage, NewsListPage, NewsCategory

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(NewsListPage)
class NewsListPageTR(TranslationOptions):
    pass


@register(NewsPage)
class NewsPageTR(TranslationOptions):
    fields = ("short_description", "body")


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
