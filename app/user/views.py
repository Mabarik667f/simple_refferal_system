from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from django.contrib.auth import get_user_model
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiResponse
from redis import Redis

from user.models import ActivatedCodeForUser, InvitationCode
from user.serializers import (
    AuthOutSerializer,
    AuthCreateSerializer,
    UserSerializer,
    ActivateCodeSerializer,
    SimpleUserSerializer,
)
from user.permissions import VerifyCodePermission

USER = get_user_model()
redis_client: Redis = settings.REDIS_CLIENT


class AuthView(generics.GenericAPIView):

    queryset = USER.objects.all()
    serializer_class = AuthCreateSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            201: OpenApiResponse(
                AuthCreateSerializer, description="Успешно создан код подтверждения"
            ),
            400: OpenApiResponse(description="Ошибка валидации"),
        }
    )
    def post(self, request: Request):
        serializer: AuthCreateSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.create(serializer.validated_data)
            return Response(
                {"code": user_data[1], "phone": user_data[0]},
                status=status.HTTP_201_CREATED,
            )
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(generics.GenericAPIView):

    queryset = USER.objects.all()
    serializer_class = AuthOutSerializer
    permission_classes = [VerifyCodePermission]

    @extend_schema(
        responses={
            201: OpenApiResponse(
                AuthOutSerializer, description="Авторизация прошла успешно"
            ),
            400: OpenApiResponse(description="Ошибка валидации"),
        }
    )
    def post(self, request: Request):
        serializer: AuthOutSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(serializer.validated_data)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveAPIView):
    queryset = USER.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


class ActivateInviteCodeView(generics.CreateAPIView):

    queryset = InvitationCode.objects.all()
    serializer_class = ActivateCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request: Request):
        serializer: ActivateCodeSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UsersByInviteCodeView(generics.ListAPIView):

    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        invitation_code = InvitationCode.objects.get(user=user)
        activated_codes = ActivatedCodeForUser.objects.filter(
            invitation_code=invitation_code
        ).select_related("user")
        user_ids = [obj.user.pk for obj in activated_codes]
        return USER.objects.filter(pk__in=user_ids)
