from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from home.models import Workshop
from payments.models import Plan


class MembershipType(ClusterableModel):
    name = models.TextField(verbose_name=_("Ime članstva"))
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Plačilni paket"))

    def __str__(self):
        return self.name
    
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
        verbose_name_plural = _("Tipi članstva")
    

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


class Membership(models.Model):
    type = models.ForeignKey(MembershipType, on_delete=models.CASCADE, null=True, blank=True)
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

    def __str__(self):
        return f"{self.type} ({self.active}): {self.valid_from} - {self.valid_to}"


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


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="elektronski naslov")
    membership = models.ForeignKey(Membership, null=True, blank=True, on_delete=models.SET_NULL)
    prima_id = models.IntegerField(null=True)
    address_1 = models.CharField(max_length=200, blank=True)
    address_2 = models.CharField(max_length=200, blank=True)
    legal_person_name = models.CharField(max_length=200, blank=True)
    legal_person_address_1 = models.CharField(max_length=200, blank=True)
    legal_person_address_2 = models.CharField(max_length=200, blank=True)
    legal_person_tax_number = models.CharField(max_length=200, blank=True)
    legal_person_vat = models.CharField(max_length=200, blank=True)
    public_profile = models.BooleanField(default=False)
    public_username = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    # categories
    # images
    workshops_attended = models.ManyToManyField(Workshop, verbose_name="Opravljena usposabljanja")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_valid_subscription(self):
        return self.payments.all().is_active_subscription()
    
    def get_valid_tokens(self):
        return self.payments.all().get_valid_tokens()
    
    def get_available_workshops(self):
        return self.payments.all().get_available_workshops()


class BookingToken(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.token}"
