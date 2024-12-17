from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import EventCategory, EventListArchivePage, EventListPage, EventPage


@register(EventPage)
class EventPageTR(TranslationOptions):
    fields = ("body", "tag", "location", "notice")


@register(EventListArchivePage)
class EventListArchivePageTR(TranslationOptions):
    pass


@register(EventListPage)
class EventListPageTR(TranslationOptions):
    pass


@register(EventCategory)
class EventCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
