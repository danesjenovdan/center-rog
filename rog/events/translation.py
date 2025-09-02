from .models import (EventPage, EventListArchivePage, EventListPage,
    EventCategory, EventExtraRegistrationQuestion)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


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


@register(EventExtraRegistrationQuestion)
class EventExtraRegistrationQuestionTR(TranslationOptions):
    fields = ("question", "choices",)