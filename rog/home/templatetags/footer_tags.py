import random

from django import template
from home.models.image import CustomImage
from home.models.settings import MetaSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_random_image(context):
    meta_settings = MetaSettings.load(request_or_site=context.request)
    random_image = None

    images = meta_settings.footer_random_images.raw_data
    if images:
        random_choice = random.choice(images)
        random_image_id = random_choice["value"]["image"]
        random_image = CustomImage.objects.get(id=random_image_id)

    return random_image
