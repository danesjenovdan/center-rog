from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


from home.models import CustomImage, LabPage


class Tool(Orderable, ClusterableModel):
    name = models.TextField()
    image = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    # lab = models.ForeignKey(
    #     LabPage, on_delete=models.CASCADE, related_name="+")
    lab = ParentalKey(LabPage, on_delete=models.CASCADE, related_name="related_tools")

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        # InlinePanel("related_trainings", label="Related tools"),
        InlinePanel("related_tool_specifications", label=_("Specifikacija"))
    ]


class Training(models.Model):
    name = models.TextField(verbose_name=_("Usposabljanje"))
    # tool = ParentalKey(Tool, on_delete=models.CASCADE, related_name="related_trainings")

    panels = [
        FieldPanel("name"),
    ]


class ToolSpecification(Orderable):
    name = models.TextField(verbose_name=_("Specifikacija"))
    value = models.TextField(verbose_name=_("Vrednost"))
    tool = ParentalKey(Tool, on_delete=models.CASCADE, related_name="related_tool_specifications")

    panels = [
        FieldPanel("name"),
        FieldPanel("value"),
    ]

