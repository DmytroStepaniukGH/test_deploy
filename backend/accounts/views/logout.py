from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.contrib.auth import logout

from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=['Users'],
)
class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': "Logout successful"})