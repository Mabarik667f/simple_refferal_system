from django.urls import path

from user.views import (
    AuthView,
    UsersByInvitationCodeView,
    CurrentUserView,
    VerifyCodeView,
    UserView,
    ActivateInviteCodeView
)

urlpatterns = [
    path("auth/", AuthView.as_view(), name="auth"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify-code"),
    path("activate-invitation-code/", ActivateInviteCodeView.as_view(), name="activate-invitation-code"),
    path("<int:pk>/", UserView.as_view(), name="get-user"),
    path("me/", CurrentUserView.as_view(), name="me"),
    path("list/", UsersByInvitationCodeView.as_view(), name="list")
]
