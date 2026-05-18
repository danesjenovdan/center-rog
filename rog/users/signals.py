import logging

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from users.prima_api import PrimaApi

from .models import User

logger = logging.getLogger(__name__)
prima_api = PrimaApi()


@receiver(m2m_changed, sender=User.workshops_attended.through)
def sync_user_workshops_attended_to_prima(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action != "post_add" or not pk_set:
        return

    user = instance
    if not user.prima_id:
        return

    workshops = model.objects.filter(pk__in=pk_set).only("id", "prima_id")
    for workshop in workshops:
        if not workshop.prima_id:
            continue

        try:
            logger.info(
                "Syncing workshops_attended change for user %s and workshop %s to Prima",
                user.pk,
                workshop.pk,
            )
            prima_api.addUserToGroup(user.prima_id, workshop.prima_id)
        except Exception:
            logger.exception(
                "Failed to sync workshops_attended change for user %s and workshop %s to Prima",
                user.pk,
                workshop.pk,
            )
