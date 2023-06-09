from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from accounts.serializers.registration import RegistrationSerializer
from accounts.serializers.registration import ConfirmRegistrationSerializer
from accounts.tasks import send_email_for_registration_confirm
from accounts.models import User


@extend_schema(
    tags=['Users'],
)
class RegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = get_user_model()
        if serializer.is_valid():
            if User.objects.filter(email=request.data['email']).exists():
                return Response(
                    {"error": "User with this email is already registered."},
                    status=status.HTTP_409_CONFLICT
                )
            else:
                user = serializer.save()
                send_email_for_registration_confirm.apply_async(args=(user.pk,))
                return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['Users'],
)
class ConfirmRegistrationView(CreateAPIView):
    serializer_class = ConfirmRegistrationSerializer
    authentication_classes = []
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)