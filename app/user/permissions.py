from rest_framework import permissions
from django.conf import settings

redis_client = settings.REDIS_CLIENT

class VerifyCodePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.data.get("code") == redis_client.get(request.data.get("phone")).decode('utf-8')
