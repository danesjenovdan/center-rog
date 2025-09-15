from .models import UserInterest, MembershipTypeSpecification, MembershipType
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(UserInterest)
class UserInterestTranslationOptions(TranslationOptions):
    fields = (
        "name",
    )


@register(MembershipTypeSpecification)
class MembershipTypeSpecificationTranslationOptions(TranslationOptions):
    fields = (
        "name",
    )


@register(MembershipType)
class MembershipTypeTranslationOptions(TranslationOptions):
    fields = (
        "name",
    )

