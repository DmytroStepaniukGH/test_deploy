from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from accounts.serializers.login import LoginSerializer # noqa


@extend_schema(
    tags=['Users'],
)
class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = LoginSerializer

    @csrf_exempt
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'error': 'Both "email" and "password" are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({'error': 'Access denied: wrong email or password.'},
                            status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({'token': token.key,
                         'id': user.patient.id if not user.is_doctor else user.doctor.id,
                         'user_id': user.id,
                         'is_doctor': user.is_doctor},
                        status=status.HTTP_200_OK)
