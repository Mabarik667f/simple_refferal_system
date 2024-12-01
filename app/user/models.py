from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser):
    password = None
    phone = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(regex=r"^7\d{10}$", code="invalid_phone"),
        ],
    )

    USERNAME_FIELD = "phone"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(phone__regex=r"^7\d{10}$"),
                name="user_phone_regex_constraint",
            ),
            models.UniqueConstraint(fields=["phone"], name="unique_phone_constraint"),
        ]

    activated_code = models.ManyToManyField(
        to="InvitationCode",
        through="ActivatedCodeForUser",
    )
    objects = models.Manager()


class InvitationCode(models.Model):
    user = models.OneToOneField(
        to=CustomUser, on_delete=models.CASCADE, primary_key=True
    )
    code = models.CharField(max_length=6, db_index=True, unique=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["code"], name="code_constraint")]

    objects = models.Manager()


class ActivatedCodeForUser(models.Model):
    user = models.OneToOneField(
        to=CustomUser, on_delete=models.CASCADE, primary_key=True
    )
    invitation_code = models.ForeignKey(to=InvitationCode, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "invitation_code"],
                name="unique_user_code",
                violation_error_message="Этот пользователь уже активировал код!",
            )
        ]

    objects = models.Manager()
