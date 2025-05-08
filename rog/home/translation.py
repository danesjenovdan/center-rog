from .models import HomePage, ContentPage
from .models.pages import (
    StudioListPage,
    MarketStoreListPage,
    ResidenceListPage,
    LabListPage,
    LabPage,
    WorkingStationPage,
    LibraryPage,
    StudioPage,
    ResidencePage,
    MarketStorePage,
    ResidenceArchiveListPage,
    StudioArchiveListPage,
)
from .models.base_pages import BasicTextPage
from .models.workshop import Workshop
from .models.settings import MetaSettings
from .models.tool import Tool, ToolSpecification

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = ("body",)


@register(ContentPage)
class ContentPageTR(TranslationOptions):
    fields = ("body",)


@register(StudioListPage)
class StudioListPageTR(TranslationOptions):
    fields = ("intro_text",)


@register(MarketStoreListPage)
class MarketStoreListPageTR(TranslationOptions):
    fields = ("intro_text",)


@register(ResidenceListPage)
class ResidenceListPageTR(TranslationOptions):
    fields = ("intro_text",)


@register(ResidenceArchiveListPage)
class ResidenceArchiveListPageTR(TranslationOptions):
    pass


@register(StudioArchiveListPage)
class StudioArchiveListPageTR(TranslationOptions):
    pass


@register(LabListPage)
class LabListPageTR(TranslationOptions):
    fields = ("intro_text",)


class ObjectProfilePageTR(TranslationOptions):
    fields = (
        "description",
        "image_description",
        "contact_description",
        "working_hours",
    )


@register(ToolSpecification)
class ToolSpecificationTR(TranslationOptions):
    fields = ("name", "value")


@register(Tool)
class ToolTR(TranslationOptions):
    fields = ("name",)
    related_fields = ("related_tool_specifications",)


@register(LabPage)
class LabPageTR(TranslationOptions):
    fields = ("description", "button", "working_hours", "notice")
    related_fields = ("related_tools",)


@register(WorkingStationPage)
class WorkingStationPageTR(TranslationOptions):
    fields = ("description", "modules", "tag",)


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


@register(BasicTextPage)
class BasicTextPageTR(TranslationOptions):
    fields = ("body",)


@register(Workshop)
class HomePageTR(TranslationOptions):
    fields = ("name",)


@register(MetaSettings)
class MetaSettingsTR(TranslationOptions):
    fields = (
        "organization_working_hours_title",
        "organization_working_hours",
        "organization_notice",
        "labs_working_hours_title",
        "labs_working_hours",
        "footer_links",
        "footer_logos",
        "header_marquee",
    )
