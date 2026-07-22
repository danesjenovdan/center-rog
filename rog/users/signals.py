import logging

from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.db import transaction

from users.prima_api import PrimaApi

from .models import User, Organization

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


@receiver(pre_save, sender=User)
def user_organization_changed(sender, instance, **kwargs):
    # Pri create je prejsnja organizacija vedno None.
    if not instance.pk:
        old_org_id = None
    else:
        old_org_id = (
            sender.objects.filter(pk=instance.pk)
            .values_list("organization_id", flat=True)
            .first()
        )
    new_org_id = instance.organization_id

    if old_org_id == new_org_id:
        return

    def _after_commit():
        old_org = (
            Organization.objects.filter(pk=old_org_id).first() if old_org_id else None
        )
        new_org = (
            Organization.objects.filter(pk=new_org_id).first() if new_org_id else None
        )
        instance.on_organization_changed(old_org, new_org)

    transaction.on_commit(_after_commit)


@receiver(pre_save, sender=Organization)
def cache_previous_organization_owner(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_owner_id = None
    else:
        instance._old_owner_id = (
            sender.objects.filter(pk=instance.pk).values_list("owner_id", flat=True).first()
        )


@receiver(post_save, sender=Organization)
def sync_organization_owner_to_user(sender, instance, **kwargs):
    old_owner_id = getattr(instance, "_old_owner_id", None)

    new_owner_id = instance.owner_id

    if old_owner_id == new_owner_id:
        return

    def _after_commit():
        # Remove organization from previous owner only if it still points to this org.
        if old_owner_id:
            User.objects.filter(pk=old_owner_id, organization_id=instance.pk).update(
                organization=None
            )

        # Assign this organization to new owner.
        if new_owner_id:
            User.objects.filter(pk=new_owner_id).exclude(organization_id=instance.pk).update(
                organization_id=instance.pk
            )

    transaction.on_commit(_after_commit)
