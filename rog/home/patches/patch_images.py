from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from taggit.models import Tag
from wagtail.images import get_image_model


def get_all_tags_for_model(model):
    """Return a queryset of all tags used on this model class"""
    content_type = ContentType.objects.get_for_model(model)
    return (
        Tag.objects.exclude(name="__user_gallery__")
        .filter(taggit_taggeditem_items__content_type=content_type)
        .annotate(item_count=Count("taggit_taggeditem_items"))
        .order_by("-item_count")
    )


def patch_images_index_view():
    from wagtail.images.views import images
    from django.core.paginator import Paginator

    OldIndexView = images.IndexView

    class NewIndexView(OldIndexView):
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            # show all tags instead of just the popular ones
            context["popular_tags"] = get_all_tags_for_model(get_image_model())

            # filter out the user gallery tag
            old_images_page = context["images"]
            old_paginator = old_images_page.paginator
            old_images = old_paginator.object_list
            new_images = old_images.exclude(tags__name="__user_gallery__")
            new_paginator = Paginator(
                new_images,
                old_paginator.per_page,
                old_paginator.orphans,
                old_paginator.allow_empty_first_page,
            )
            new_images_page = new_paginator.get_page(old_images_page.number)
            context["images"] = new_images_page

            return context

    images.IndexView = NewIndexView
