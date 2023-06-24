from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import datetime


class ActiveAtQuerySet(models.QuerySet):
    def is_active_subscription(self):
        now = datetime.now()
        return True if self.filter(
            plna__subscription=True,
            active_to__gte=now,
        ) else False

    def get_valid_tokens(self):
        timestamp = datetime.now()
        return self.tokens.filter(
            valid_from__lte=timestamp,
            valid_to__gte=timestamp,
            is_used=False,
        )


class Timestampable(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


# payments
class Plan(Timestampable):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    is_subscription = models.BooleanField(default=False)
    valid_from = models.DateTimeField(
        auto_now_add=True, help_text=_("When the plan starts"),
        null=True,
        blank=True
    )
    valid_to = models.DateTimeField(
        help_text=_("When the plan expires"),
        null=True,
        blank=True
    )
    duration = models.IntegerField(
        help_text=_("How many days the plan items lasts")
    )
    tokens = models.IntegerField(
        help_text=_("How many tokens a user gets"),
        default=0
    )
    week_token_limit = models.IntegerField(
        help_text=_("How many tokens a user can use in a week"),
        null=True,
        blank=True
    )
    month_token_limit = models.IntegerField(
        help_text=_("How many tokens a user can use in a month"),
        null=True,
        blank=True
    )
    year_token_limit = models.IntegerField(
        help_text=_("How many tokens a user can use in a year"),
        null=True,
        blank=True
    )
    workshops = models.IntegerField(
        help_text=_("How many workshops the user receives"),
        null=True,
        blank=True,
        default=0
    )

    def __str__(self):
        return f"{self.name} - {self.price} - {self.duration}"


class Payment(Timestampable):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SUCCESS = "SUCCESS", _("Success")
        ERROR = "ERROR", _("Error")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="Select a user",
    )
    amount = models.IntegerField()
    successed_at = models.DateTimeField(null=True, blank=True)
    errored_at = models.DateTimeField(null=True, blank=True)
    active_to = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When subscription expires",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    info = models.TextField(blank=True, null=True)
    plan = models.ForeignKey(
        "Plan",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="Select a plan",
    )

    objects = ActiveAtQuerySet.as_manager()

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.created_at}"
    
    def history_name(self):
        return f"{self.plan.name}"


class Token(Timestampable):
    class Type(models.TextChoices):
        LAB = "LAB", _("Lab")
        WORKSHOP = "WORKSHOP", _("Workshop")
    type_of = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.LAB
    )
    valid_from = models.DateField(auto_now_add=True)
    valid_to = models.DateField(auto_now_add=True)
    payment = models.ForeignKey(
        Payment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="tokens",
    )
    # TODO: connect (FK) this field to point of use (probably to reservation)
    used_for = models.CharField(max_length=100, null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.token} - {self.date}"
