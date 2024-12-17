from django import template
from django.conf import settings

register = template.Library()


@register.filter
def strip_language(value):
    """
    We are taking off the first (leftmost) item in the path if it is in
    the language list
    """
    parts = value.strip("/").split("/")
    language = parts.pop(0)
    if language in [lang[0] for lang in settings.LANGUAGES]:
        return "/{}".format("/".join(parts))
    return value
