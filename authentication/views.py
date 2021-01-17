import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from decouple import config

from rest_framework import generics, views
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers import RegistrationSerializer
from authentication.serializers import EmailVerificationSerializer
from authentication.serializers import LoginSerializer

from authentication.serializers import LogoutSerializer
from authentication.models import User
from authentication.utils import Util


class RegistrationView(generics.GenericAPIView):
    """
    View for user registration
    """

    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user=user).access_token
        current_site = get_current_site(request=request).domain
        relative_link = reverse("verify-email")
        abs_url = f"http://{current_site}{relative_link}?token={str(token)}"

        email_body = (
            f"Hi {user.username}, use the link below to verify your email \n {abs_url}"
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    """
    View for confirm email with token
    """

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, config("SECRET_KEY"), algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {
                    "msg": "Successfully activated",
                },
                status=status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "error": "Activation link expired",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except jwt.DecodeError:
            return Response(
                {
                    "error": "Invalid token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginApiView(generics.GenericAPIView):
    """
    View for login user
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutApiView(generics.GenericAPIView):
    """
    View for user logout
    """

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)