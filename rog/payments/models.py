from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from datetime import datetime, timezone

from .pantheon import create_ident, create_move
from behaviours.models import Timestampable

import random
from string import ascii_uppercase


class PaymentItemType(models.TextChoices):
    CLANARINA = "clanarina", _("Clanarina")
    UPORABNINA = "uporabnina", _("Uporabnina")
    EVENT = "event", _("Dogodek")


class ActiveAtQuerySet(models.QuerySet):
    def get_last_active_subscription_payment_plan(self):
        now = datetime.now()
        active_payments = self.filter(
            items__payment_item_type=PaymentItemType.UPORABNINA,
            successed_at__isnull=False,
            payment_plans__valid_to__gte=now,
        )
        if active_payments:
            return active_payments.latest('successed_at').payment_plans.all().filter(plan__payment_item_type=PaymentItemType.UPORABNINA).last()
        return None

    def get_valid_tokens(self):
        timestamp = datetime.now()
        return Token.objects.filter(
            valid_from__lte=timestamp,
            valid_to__gte=timestamp,
            is_used=False,
            type_of=Token.Type.LAB,
            payment__in=self
        )

    def get_available_workshops(self):
        timestamp = datetime.now()
        return Token.objects.filter(
            valid_from__lte=timestamp,
            valid_to__gte=timestamp,
            is_used=False,
            type_of=Token.Type.WORKSHOP,
            payment__in=self
        )






# payments
class Plan(Timestampable):
    name = models.CharField(max_length=100, verbose_name=_("Ime paketa"), help_text=_("Npr. letna uporabnina"),)
    discounted_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("Discounted price"),
        help_text=_("Price for younger than 26 years old and older than 65")
    )
    is_subscription = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_("Cena"))
    description = models.CharField(max_length=300, verbose_name=_("Opis"))
    description_item_1 = models.CharField(max_length=300, verbose_name=_("Postavka 1"), blank=True, null=True)
    description_item_2 = models.CharField(max_length=300, verbose_name=_("Postavka 2"), blank=True, null=True)
    description_item_3 = models.CharField(max_length=300, verbose_name=_("Postavka 3"), blank=True, null=True)
    description_item_4 = models.CharField(max_length=300, verbose_name=_("Postavka 4"), blank=True, null=True)
    description_item_5 = models.CharField(max_length=300, verbose_name=_("Postavka 5"), blank=True, null=True)
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
        verbose_name=_("Koliko dni traja paket?"),
        # help_text=_("How many days the plan items lasts")
    )
    tokens = models.IntegerField(
        verbose_name=_("Koliko žetonov dobi uporabnik?"),
        # help_text=_("How many tokens a user gets"),
        default=0
    )
    week_token_limit = models.IntegerField(
        verbose_name=_("Tedenska omejitev porabe žetonov"),
        # help_text=_("How many tokens a user can use in a week"),
        null=True,
        blank=True
    )
    month_token_limit = models.IntegerField(
        verbose_name=_("Mesečna omejitev porabe žetonov"),
        # help_text=_("How many tokens a user can use in a month"),
        null=True,
        blank=True
    )
    year_token_limit = models.IntegerField(
        verbose_name=_("Letna omejitev porabe žetonov"),
        # help_text=_("How many tokens a user can use in a year"),
        null=True,
        blank=True
    )
    workshops = models.IntegerField(
        verbose_name=_("Koliko delavnic dobi uporabnik v paketu?"),
        # help_text=_("How many workshops the user receives"),
        null=True,
        blank=True,
        default=0
    )
    pantheon_ident_id = models.CharField(
        max_length=16,
        unique=True,
        help_text=_("Unique ident id for Pantheon without dashes and spaces")
    )
    payment_item_type = models.CharField(
        max_length=20,
        choices=PaymentItemType.choices,
        default=PaymentItemType.CLANARINA,
    )
    vat = models.IntegerField(default=22) # TODO: če se bo kdaj rabilo 9.5% ddv je treba spremenit v DecimalField

    def __str__(self):
        return f"{self.name}"

    def get_pantheon_ident_id(self):
        return self.pantheon_ident_id.replace('-', ' ')

    panels = [
        FieldPanel("name"),
        FieldPanel("price"),
        FieldPanel("discounted_price"),
        FieldPanel("is_subscription"),
        FieldPanel("valid_to"),
        MultiFieldPanel(
            [
                FieldPanel("description"),
                FieldPanel("description_item_1"),
                FieldPanel("description_item_2"),
                FieldPanel("description_item_3"),
                FieldPanel("description_item_4"),
                FieldPanel("description_item_5"),
            ],
            heading=_("Opis paketa")
        ),
        FieldPanel("duration"),
        FieldPanel("tokens"),
        FieldPanel("week_token_limit"),
        FieldPanel("month_token_limit"),
        FieldPanel("year_token_limit"),
        FieldPanel("workshops"),
        FieldPanel("pantheon_ident_id"),
        FieldPanel("payment_item_type"),
    ]

    class Meta:
        verbose_name = _("Plačilni paket")
        verbose_name_plural = _("Uporabniki - plačilni paketi")

    def save(self, *args, **kwargs):
        if self.id == None:
            # create ident by name
            if self.pantheon_ident_id == None:
                self.pantheon_ident_id = slugify(self.name)[:16]
            super().save(*args, **kwargs)
            create_ident(self)
        else:
            super().save(*args, **kwargs)

class PaymentPlanEvent(models.Model):
    payment_item_type = models.CharField(
        max_length=20,
        choices=PaymentItemType.choices,
        default=PaymentItemType.CLANARINA,
    )

    payment = models.ForeignKey('Payment', related_name="payment_plans", on_delete=models.CASCADE)
    plan = models.ForeignKey('Plan', related_name="payment_plans", on_delete=models.CASCADE, null=True, blank=True)
    event_registration = models.ForeignKey('events.EventRegistration', related_name="payment_plans", on_delete=models.CASCADE, null=True, blank=True)

    plan_name = models.CharField(max_length=100, verbose_name=_("Ime paketa na dan nakupa"), help_text=_("Npr. letna uporabnina"),)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    promo_code = models.ForeignKey(
        "PromoCode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment_plans",
        help_text="The promo code used for this payment plan",
    )
    valid_to = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When subscription expires",
    )
    notification_30_sent = models.BooleanField(default=False)
    notification_7_sent = models.BooleanField(default=False)
    notification_1_sent = models.BooleanField(default=False)


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
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    successed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When payment was successed",
    )
    errored_at = models.DateTimeField(null=True, blank=True)
    payment_done_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Done at"),
        help_text="When payment was done",)
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
    items = models.ManyToManyField(
        'Plan',
        help_text="Items in payment",
        related_name="payments",
        through=PaymentPlanEvent,
    )
    user_was_eligible_to_discount = models.BooleanField(default=False)
    objects = ActiveAtQuerySet.as_manager()
    saved_in_pantheon = models.BooleanField(
        default=False,
        help_text=_("Ali račun že shranjen v Pantheon ali preprečite shranjevanje računa v Pantheon")
    )
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    membership = models.ForeignKey('users.Membership', null=True, blank=True, on_delete=models.SET_NULL)
    panels = [
        FieldPanel("user"),
        FieldPanel("amount"),
        FieldPanel("successed_at"),
        FieldPanel("payment_done_at"),
        FieldPanel("errored_at"),
        FieldPanel("active_to"),
        FieldPanel("status"),
        FieldPanel("info"),
        FieldPanel("user_was_eligible_to_discount"),
        FieldPanel("items"),
        FieldPanel("saved_in_pantheon"),
    ]

    class Meta:
        verbose_name = _("Naročilo")
        verbose_name_plural = _("Naročila")

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.created_at}"

    def history_name(self):
        return f"{self.items.first().name}"

    def save(self, *args, **kwargs):
        if self.saved_in_pantheon == False and self.successed_at:
            super().save(*args, **kwargs)
            print(create_move(self))
            self.saved_in_pantheon = True
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


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
        return f"{self.type_of} - {self.is_used}"

def generate_promo_code(length: int = 10) -> str:
        characters = ascii_uppercase + '0123456789'
        return ''.join(random.choice(characters) for i in range(length))

class PromoCode(Timestampable):
    code = models.CharField(max_length=100, null=False, blank=False, default=generate_promo_code)
    valid_to = models.DateTimeField(
        help_text=_("When does the code expire?"),
        null=False,
        blank=False,
    )
    percent_discount = models.IntegerField(null=False, blank=False)
    payment_item_type = models.CharField(
        max_length=20,
        choices=PaymentItemType.choices,
        default=PaymentItemType.CLANARINA,
    )
    single_use = models.BooleanField(blank=False, null=False)
    number_of_uses = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f"{self.code}"

    @staticmethod
    def check_code_validity(code_string: str, payment_plan: PaymentPlanEvent) -> bool:
        code_filter = PromoCode.objects.filter(code=code_string)

        if code_filter.count() == 1:
            code = code_filter.first()
            now = datetime.now().replace(tzinfo=timezone.utc)

            if code.valid_to < now:
                return False

            if code.single_use and code.number_of_uses > 0:
                return False

            if code.payment_item_type != payment_plan.payment_item_type:
                return False

            if payment_plan.promo_code == code:
                return False

            return True

        if code_filter.count() == 0:
            return False

        raise Exception(f"Weird number of codes: {code}.")

    def use_code(self) -> None:
        self.number_of_uses += 1
        self.save()
