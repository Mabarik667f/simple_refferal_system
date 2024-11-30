from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.conf import settings

USER = get_user_model()

class JWTAuthBackend(BaseBackend):

    def get_user(self, user_id):
        try:
            return USER.objects.get(pk=user_id)
        except USER.DoesNotExist:
            return None

    def authenticate(self, request, **kwargs):
        print(request)
        try:
            user = USER.objects.get(phone=request.phone)
        except USER.DoesNotExist:
            return None

        if settings.REDIS_CLIENT.get(user.phone).decode("utf-8") == request.verify_code:
            return user
        else:
            return None
