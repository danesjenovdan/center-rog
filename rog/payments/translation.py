from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import Plan


@register(Plan)
class PlanTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
        "description_item_1",
        "description_item_2",
        "description_item_3",
        "description_item_4",
        "description_item_5",
    )
