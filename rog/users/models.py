from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class Timestampable(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Membership(models.Model):
    start_day = models.DateField()
    end_day = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_day} - {self.end_day}"


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
    email = models.EmailField(unique=True)
    membership = models.ForeignKey(Membership, null=True, blank=True, on_delete=models.SET_NULL)
    prima_id = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, blank=True) # ne rabimo?
    address_1 = models.CharField(max_length=200, blank=True)
    address_2 = models.CharField(max_length=200, blank=True)
    public_profile = models.BooleanField(default=False)
    public_username = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    # categories
    # images

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# payments

class Plan(Timestampable):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    valid_from = models.DateTimeField(
        auto_now_add=True, help_text=_("When the plan starts")
    )
    valid_to = models.DateTimeField(
        help_text=_("When the plan expires")
    )
    duration = models.IntegerField(
        help_text=_("How many days the plan items lasts")
    )
    tokens = models.IntegerField(
        help_text=_("How many tokens a user gets")
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
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.price} - {self.duration}"


class Payment(Timestampable):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SUCCESS = "SUCCESS", _("Success")
        ERROR = "ERROR", _("Error")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    finished_at = models.DateTimeField(null=True, blank=True)
    errored_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    info = models.TextField(blank=True, null=True)
    plan = models.ForeignKey(
        'Plan',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="Select a plan or leave blank to purchase tokens",
    )

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.date_created}"


class Token(Timestampable):
    valid_from = models.DateField(auto_now_add=True)
    valid_to = models.DateField(auto_now_add=True)
    payment = models.ForeignKey(
        Payment, null=True, blank=True, on_delete=models.CASCADE
    )
    # TODO: connect (FK) this field to point of use
    used_for = models.CharField(max_length=100, null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.token} - {self.date}"
