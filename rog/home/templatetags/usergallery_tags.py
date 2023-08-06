from django import template

register = template.Library()


@register.filter
def gallery_data(field):
    stream_value = field.value()
    if stream_value is None:
        return []

    images = []

    for child in stream_value:
        if child.block_type == "image":
            images.append(
                {
                    "block_id": child.id,
                    "image_id": child.value.id,
                    "url": child.value.file.url,
                    "name": child.value.file.name,
                    "size": child.value.file.size,
                    "width": child.value.file.width,
                    "height": child.value.file.height,
                }
            )

    return images
