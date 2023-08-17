from .models import HomePage, ContentPage
from .models.pages import (StudioListPage, MarketStoreListPage, ResidenceListPage, LabListPage, LabPage,
    LibraryPage, StudioPage, ResidencePage, MarketStorePage, ResidenceArchiveListPage, StudioArchiveListPage
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'body',
    )


@register(ContentPage)
class ContentPageTR(TranslationOptions):
    fields = (
        'body',
    )


@register(StudioListPage)
class StudioListPageTR(TranslationOptions):
    fields = (
        'intro_text',
    )


@register(MarketStoreListPage)
class MarketStoreListPageTR(TranslationOptions):
    fields = (
        'intro_text',
    )


@register(ResidenceListPage)
class ResidenceListPageTR(TranslationOptions):
    fields = (
        'intro_text',
    )


@register(ResidenceArchiveListPage)
class ResidenceArchiveListPageTR(TranslationOptions):
    pass


@register(StudioArchiveListPage)
class StudioArchiveListPageTR(TranslationOptions):
    pass


@register(LabListPage)
class LabListPageTR(TranslationOptions):
    fields = (
        'intro_text',
    )


class ObjectProfilePageTR(TranslationOptions):
    fields = (
        'description',
        'image_description',
        'contact_description'
    )


@register(LabPage)
class LabPageTR(ObjectProfilePageTR):
    pass


@register(LibraryPage)
class LibraryPageTR(ObjectProfilePageTR):
    pass


@register(StudioPage)
class StudioPageTR(ObjectProfilePageTR):
    pass


@register(ResidencePage)
class ResidencePageTR(ObjectProfilePageTR):
    pass


@register(MarketStorePage)
class MarketStorePageTR(ObjectProfilePageTR):
    pass
