from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from taggit.models import Tag
from wagtail.images import get_image_model


def get_all_tags_for_model(model):
    """Return a queryset of all tags used on this model class"""
    content_type = ContentType.objects.get_for_model(model)
    return (
        Tag.objects.filter(taggit_taggeditem_items__content_type=content_type)
        .annotate(item_count=Count("taggit_taggeditem_items"))
        .order_by("-item_count")
    )


def patch_images_index_view():
    from wagtail.images.views import images

    OldIndexView = images.IndexView

    class NewIndexView(OldIndexView):
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["popular_tags"] = get_all_tags_for_model(get_image_model())
            return context

    images.IndexView = NewIndexView
