from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, InlinePanel


class Workshop(models.Model):
    name = models.TextField(verbose_name=_("Ime usposabljanja"))

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Usposabljanje za orodje")
        verbose_name_plural = _("Orodja - usposabljanja")
