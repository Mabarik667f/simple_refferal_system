from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.fields import RegexValidator
from time import sleep
from random import randint

from user.models import ActivatedCodeForUser, InvitationCode

USER = get_user_model()
redis_client = settings.REDIS_CLIENT


class PhoneField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [
            RegexValidator(
                regex=r"^7\d{10}$",
            ),
        ]
        kwargs["max_length"] = 11
        super().__init__(*args, **kwargs)


class VerifyCodeField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [
            RegexValidator(regex=r"^\d+$", message="Код - 4 числа"),
        ]
        kwargs["min_length"] = 4
        kwargs["max_length"] = 4
        super().__init__(*args, **kwargs)


class AuthSerializer(serializers.ModelSerializer):
    code = VerifyCodeField()

    class Meta:
        model = USER
        fields = ["phone", "code"]
        read_only_fields = ["code"]


class AuthCreateSerializer(AuthSerializer):

    code = VerifyCodeField(read_only=True)
    phone = PhoneField()

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

    phone = PhoneField(write_only=True)
    code = VerifyCodeField(write_only=True)

    class Meta(AuthSerializer.Meta):
        fields = ["phone", "token", "code"]

    def create(self, validated_data: dict) -> dict[str, str]:
        phone = validated_data.get("phone", "")
        user = USER.objects.get(phone=phone)
        token, _ = Token.objects.get_or_create(user=user)
        data = {"token": token.key}
        redis_client.delete(phone)
        return data


class SimpleUserSerializer(serializers.ModelSerializer):
    phone = PhoneField(read_only=True)

    class Meta:
        model = USER
        fields = ["phone"]


class UserSerializer(serializers.ModelSerializer):

    my_code = serializers.SerializerMethodField()
    activated_code = serializers.SerializerMethodField()

    class Meta:
        model = USER
        fields = ["id", "phone", "my_code", "activated_code"]

    def get_my_code(self, obj):
        invitation_code = get_object_or_404(InvitationCode, user=obj)
        return invitation_code.code

    def get_activated_code(self, obj):
        try:
            activated_code = ActivatedCodeForUser.objects.get(pk=obj)
            invitation_code = InvitationCode.objects.get(
                user=activated_code.invitation_code
            )
            return invitation_code.code
        except ActivatedCodeForUser.DoesNotExist:
            return None


class ActivateCodeSerializer(serializers.ModelSerializer):
    invitation_code = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())

    class Meta:
        model = ActivatedCodeForUser
        fields = ["invitation_code", "user"]
        write_only = ["invitation_code", "user"]

    def validate_invitation_code(self, code: str) -> str:
        try:
            return InvitationCode.objects.get(code=code).code
        except InvitationCode.DoesNotExist:
            raise serializers.ValidationError("Такого кода не существует!")

    def validate_user(self, user):
        exists = ActivatedCodeForUser.objects.filter(user=user).exists()
        if exists:
            raise serializers.ValidationError("Этот пользователь уже активировал код!")
        return user

    def validate(self, attrs: dict) -> dict:
        try:
            if InvitationCode.objects.get(
                user=attrs["user"], code=attrs["invitation_code"]
            ):
                raise serializers.ValidationError(
                    {"invitation_code": "Данный код принадлежит текущему пользователю!"}
                )
            return attrs
        except InvitationCode.DoesNotExist:
            return attrs

    def create(self, validated_data: dict) -> None:
        user_pk = validated_data["user"]
        code = validated_data["invitation_code"]
        code_pk = InvitationCode.objects.get(code=code)
        ActivatedCodeForUser.objects.create(user=user_pk, invitation_code=code_pk)
