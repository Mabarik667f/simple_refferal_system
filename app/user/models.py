from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    password = None
    phone = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        validators=[
        RegexValidator(
            regex=r'^7\d{10}$',
            code="invalid_phone"
        ),
    ])
    invite_code = models.CharField(max_length=6, db_index=True, unique=True)
    activated_invited_code = models.CharField(max_length=6, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["invite_code"]

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(phone__regex=r"^7\d{10}$"),
                name="user_phone_regex_constraint"
            ),
            models.UniqueConstraint(
                fields=["phone", "invite_code"],
                name="unique_phone_invite_code_constraint"
            )
        ]

    objects = models.Manager()
