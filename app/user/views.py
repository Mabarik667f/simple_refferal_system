from re import A
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, permissions, authentication, generics, status

from django.contrib.auth import get_user_model
from django.conf import settings
from redis import Redis

from user.serializers import AuthOutSerializer, AuthCreateSerializer, UserSerializer
from user.permissions import VerifyCodePermission

USER = get_user_model()
redis_client: Redis = settings.REDIS_CLIENT

class AuthView(generics.GenericAPIView):

    queryset = USER.objects.all()
    serializer_class = AuthCreateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        serializer: AuthCreateSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.create(serializer.validated_data)
            return Response({"verify-code": user_data[1], "phone": user_data[0]}, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(generics.GenericAPIView):

    queryset = USER.objects.all()
    serializer_class = AuthOutSerializer
    permission_classes = [VerifyCodePermission]

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

    queryset = USER.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request: Request):
        pass


class UsersByInviteCodeView(generics.ListAPIView):

    queryset = USER.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
