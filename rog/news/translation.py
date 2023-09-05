# from .models import NewsListPage, NewsListArchivePage, NewsPage, NewsListPage
from .models import NewsListPage, NewsPage, NewsListPage

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(NewsListPage)
class NewsListPageTR(TranslationOptions):
    pass


# @register(NewsListArchivePage)
# class NewsListArchivePageTR(TranslationOptions):
#     pass


@register(NewsPage)
class NewsPageTR(TranslationOptions):
    fields = (
        'short_description',
        'body'
    )
