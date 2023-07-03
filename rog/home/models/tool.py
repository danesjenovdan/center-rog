from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from .image import CustomImage
from .pages import LabPage
from .workshop import Workshop


class Tool(Orderable, ClusterableModel):
    name = models.TextField()
    image = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    lab = ParentalKey(LabPage, on_delete=models.CASCADE, related_name="related_tools")
    required_workshop = models.ForeignKey(
        Workshop, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name=_("Zahteva usposabljanje?"))
    prima_location_id = models.IntegerField(null=True, blank=True, verbose_name=_("Prima location id"))
    prima_group_id = models.IntegerField(null=True, blank=True, verbose_name=_("Prima group id"))

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        InlinePanel("related_tool_specifications", label=_("Specifikacija")),
        FieldPanel("required_workshop"),
        FieldPanel("prima_location_id"),
        FieldPanel("prima_group_id"),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Orodje")
        verbose_name_plural = _("Orodja")


class ToolSpecification(Orderable):
    name = models.TextField(verbose_name=_("Specifikacija"))
    value = models.TextField(verbose_name=_("Vrednost"))
    tool = ParentalKey(Tool, on_delete=models.CASCADE, related_name="related_tool_specifications")

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("value"),
    ]

    class Meta:
        verbose_name = _("Specifikacija orodja")
        verbose_name_plural = _("Specifikacije orodja")
