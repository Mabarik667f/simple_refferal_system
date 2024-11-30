from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from time import sleep
from random import randint

from rest_framework.fields import RegexValidator

USER = get_user_model()
redis_client = settings.REDIS_CLIENT

# class UserSerializer(serializers.):
# pass


class AuthSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        validators=[
            RegexValidator(regex=r"^\d+$", message="Код - 4 числа"),
        ],
    )

    class Meta:
        model = USER
        fields = ["phone", "code"]
        read_only_fields = ["code"]


class AuthCreateSerializer(AuthSerializer):

    code = serializers.CharField(
        max_length=4,
        min_length=4,
        read_only=True,
        validators=[
            RegexValidator(regex=r"^\d+$", message="Код - 4 числа"),
        ],
    )

    def create(self, validated_data: dict) -> tuple[str, str]:
        phone = validated_data.get("phone", "")
        USER.objects.get_or_create(phone=phone)

        code = "".join([str(randint(0, 9)) for _ in range(4)])
        redis_client.set(phone, code)
        sleep(2)
        return (phone, code)


class AuthOutSerializer(AuthSerializer):
    token = serializers.CharField(
        source="", read_only=True, validators=[RegexValidator(regex=r"^[a-f0-9]{40}$")]
    )

    phone = serializers.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^7\d{10}$",
            ),
        ],
        write_only=True
    )

    code = serializers.CharField(
        max_length=4,
        min_length=4,
        write_only=True,
        validators=[
            RegexValidator(regex=r"^\d+$", message="Код - 4 числа"),
        ],
    )

    class Meta(AuthSerializer.Meta):
        fields = ["phone", "token", "code"]


    def create(self, validated_data: dict) -> dict[str, str]:
        phone = validated_data.get('phone', "")
        user = USER.objects.get(phone=phone)
        token, _ = Token.objects.get_or_create(user=user)
        data = {"token": token.key}
        return data
