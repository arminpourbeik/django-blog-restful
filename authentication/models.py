from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):
    """
    Database model for users in the system
    """

    class CustomAccountManager(BaseUserManager):
        """
        Manager for users
        """

        def create_superuser(
            self, email, username, first_name, last_name, password, **other_fields
        ):
            other_fields.setdefault("is_staff", True)
            other_fields.setdefault("is_superuser", True)
            other_fields.setdefault("is_active", True)

            if other_fields.get("is_staff") is not True:
                raise ValueError("Superuser must be assigned to is_staff=True.")
            if other_fields.get("is_superuser") is not True:
                raise ValueError("Superuser must be assigned to is_superuser=True.")

            return self.create_user(
                email, username, first_name, last_name, password, **other_fields
            )

        def create_user(self, email, username, password, **other_fields):
            if not email:
                raise ValueError("You must provide an email address")
            email = self.normalize_email(email=email)
            user = self.model(
                email=email,
                username=username,
                **other_fields,
            )
            user.set_password(password)
            user.save()

            return user

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomAccountManager()

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        return self.first_name

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def __str__(self) -> str:
        return self.email
