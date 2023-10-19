from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

from home.models import Workshop
from payments.models import Plan
from payments.pantheon import create_subject
from behaviours.models import Timestampable

from datetime import datetime
import random
import uuid


class MembershipType(ClusterableModel):
    name = models.TextField(verbose_name=_("Ime članstva"))
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Plačilni paket"))

    def __str__(self):
        return self.name

    @property
    def price(self):
        if self.plan:
            return self.plan.price
        return 0

    panels = [
        FieldPanel("name"),
        FieldPanel("plan"),
        InlinePanel("related_specifications", label=_("Bonitete")),
    ]

    class Meta:
        verbose_name = _("Tip članstva")
        verbose_name_plural = _("Uporabniki - tipi članstev")


class MembershipTypeSpecification(Orderable):
    name = models.TextField(verbose_name=_("Boniteta"))
    membership_type = ParentalKey(MembershipType, on_delete=models.CASCADE, related_name="related_specifications")

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name = _("Boniteta članstva")
        verbose_name_plural = _("Bonitete članstva")


class Membership(Timestampable):
    type = models.ForeignKey(MembershipType, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='memberships')
    valid_from = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    valid_to = models.DateTimeField(
        help_text=_("When the plan expires"),
        null=True,
        blank=True
    )
    active = models.BooleanField(default=False)

    notification_30_sent = models.BooleanField(default=False)
    notification_7_sent = models.BooleanField(default=False)
    notification_1_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} ({self.active}): {self.valid_from} - {self.valid_to}"


class UserInterest(models.Model):
    name = models.TextField(verbose_name=_("Ime kategorije"))

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name = _("Kategorija zanimanj uporabnikov")
        verbose_name_plural = _("Uporabniki - kategorije zanimanj")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, Timestampable):
    username = None
    email = models.EmailField(unique=True, verbose_name="elektronski naslov")
    prima_id = models.IntegerField(null=True)
    address_1 = models.CharField(max_length=200, blank=True, verbose_name="Naslov 1")
    address_2 = models.CharField(max_length=200, blank=True, verbose_name="Naslov 2")
    legal_person_receipt = models.BooleanField(default=False, verbose_name="Račun za pravno osebo")
    legal_person_name = models.CharField(max_length=200, blank=True, verbose_name="Naziv pravne osebe")
    legal_person_address_1 = models.CharField(max_length=200, blank=True, verbose_name="Naslov 1")
    legal_person_address_2 = models.CharField(max_length=200, blank=True, verbose_name="Naslov 2")
    legal_person_tax_number = models.CharField(max_length=200, blank=True, verbose_name="Davčna številka")
    legal_person_vat = models.BooleanField(default=False, verbose_name="Zavezanec za DDV")
    public_profile = models.BooleanField(default=False, verbose_name="Profil naj bo javno viden")
    public_username = models.CharField(max_length=20, blank=True, verbose_name="Uporabniško ime")
    description = models.CharField(max_length=600, blank=True, verbose_name="Opis")
    link_1 = models.URLField(blank=True, verbose_name="Povezava do spletne strani")
    link_2 = models.URLField(blank=True, verbose_name="Povezava do spletne strani")
    link_3 = models.URLField(blank=True, verbose_name="Povezava do spletne strani")
    contact = models.EmailField(blank=True, verbose_name="Kontakt")
    birth_date = models.DateField(verbose_name="Datum rojstva", null=True)
    gender = models.CharField(max_length=1, choices=(("F", "ženski"), ("M", "moški"), ("O", "drugo")), default="O", verbose_name="Spol")
    gender_other = models.CharField(max_length=200, blank=True, verbose_name="Spol (drugo)")
    # categories
    interests = models.ManyToManyField(UserInterest, verbose_name="Kategorije zanimanj")
    # images
    workshops_attended = models.ManyToManyField(Workshop, verbose_name="Opravljena usposabljanja")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    gallery = StreamField([
        ("image", ImageChooserBlock())
    ], use_json_field=True, blank=True, default=[], max_num=10, verbose_name=_("Galerija"))

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def membership(self):
        membership = self.get_last_active_membership()
        if membership:
            return membership
        else:
            return self.memberships.filter(
                Q(valid_to__gte=datetime.now()) | Q(valid_to=None),
                valid_from__lte=datetime.now(), active=True).first()

    @property
    def most_recent_membership_is_billable(self):
        last_membership = self.memberships.last()
        return last_membership.active == False and last_membership.type.price > 0

    @property
    def get_last_active_subscription_payment_plan(self):
        return self.payments.all().get_last_active_subscription_payment_plan()

    def get_last_active_membership(self):
        membership = self.memberships.filter(
            active=True
        )
        if membership:
            return membership.latest('valid_to')
        return None

    def get_last_active_billable_membership(self):
        membership = self.memberships.filter(
            active=True,
            type__plan__isnull=False
        )
        if membership:
            return membership.latest('valid_to')
        return None

    def get_valid_tokens(self):
        return self.payments.all().get_valid_tokens()

    def get_available_workshops(self):
        return self.payments.all().get_available_workshops()

    def get_pantheon_subject_id(self):
        return str(self.uuid).replace('-', '')[:30]

    def is_eligible_to_discount(self):
        # user is eligible to discount if he is younger than 26 and older than 65
        now = datetime.now()
        lower_limit = now.replace(year=now.year-26)
        upper_limit = now.replace(year=now.year-65)
        if self.birth_date == None:
            return False
        return not(lower_limit.date() > self.birth_date > upper_limit.date())

    def random_color(self):
        return random.choice(settings.COLOR_SCHEMES)[0]

    def save(self, *args, **kwargs):
        if self.id == None:
            super().save(*args, **kwargs)
            create_subject(self)
        else:
            super().save(*args, **kwargs)


class BookingToken(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.token}"
