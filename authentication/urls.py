from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify-email"),
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("logout/", views.LogoutApiView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]