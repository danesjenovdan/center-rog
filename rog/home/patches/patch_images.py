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

            # NOTE: this broke with a wagtail upgrade, would now need to override
            # "filterset_class = ImagesFilterSet" on IndexView and then override
            # the filter class.
            # https://github.com/wagtail/wagtail/blob/2ce58fed953602cf14a8478150c38ca9fce7473e/wagtail/images/views/images.py#L57
            # https://github.com/wagtail/wagtail/blob/2ce58fed953602cf14a8478150c38ca9fce7473e/wagtail/admin/filters.py#L236
            # ------------------------------------------------------------------
            # # show all tags instead of just the popular ones
            # context["popular_tags"] = get_all_tags_for_model(get_image_model())

            # filter out the user gallery tag
            old_page_obj = context["page_obj"]
            old_paginator = context["paginator"]
            old_full_object_list = old_paginator.object_list
            new_full_object_list = old_full_object_list.exclude(tags__name="__user_gallery__")
            new_paginator = Paginator(
                new_full_object_list,
                old_paginator.per_page,
                old_paginator.orphans,
                old_paginator.allow_empty_first_page,
            )
            new_images_page = new_paginator.get_page(old_page_obj.number)
            context["paginator"] = new_paginator
            context["page_obj"] = new_images_page
            context["items_count"] = len(new_full_object_list)
            context["object_list"] = new_images_page.object_list
            context["images"] = new_images_page.object_list

            return context

    images.IndexView = NewIndexView
