from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import uuid


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The email must be set."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": "This email address is already taken."},
    )
    full_name = models.CharField(_("full name"), max_length=130)
    identifier = models.CharField(
        _("identifier"),
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r"^[0-9]+$", "Only digit characters.")],
        error_messages={"unique": "This student ID is already taken."},
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("identifier",)
