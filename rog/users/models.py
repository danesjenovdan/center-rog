from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from home.models import Workshop


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
    email = models.EmailField(unique=True, verbose_name="elektronski naslov")
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
    workshops_attended = models.ManyToManyField(Workshop, verbose_name="Opravljena usposabljanja")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_valid_subscription(self):
        return self.payments.all().is_active_subscription()
    
    def get_valid_tokens(self):
        return self.payments.all().get_valid_tokens()


class BookingToken(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.token}"
