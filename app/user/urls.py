from django.urls import path

from user.views import (
    AuthView,
    UsersByInviteCodeView,
    VerifyCodeView,
    UserView,
    ActivateInviteCodeView
)

urlpatterns = [
    path("auth/", AuthView.as_view(), name="auth"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify-code"),
    path("activate-invite-code/", ActivateInviteCodeView.as_view(), name="activate-invite-code"),
    path("<int:user_id>/", UserView.as_view(), name="get-user"),
    path("list/", UsersByInviteCodeView.as_view(), name="list")
]
