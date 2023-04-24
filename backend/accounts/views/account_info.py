from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from accounts.serializers.account_info import AccountSerializer # noqa
from accounts.models import User # noqa


@extend_schema(
    tags=['Users'],
    description='Account page.'
)
class AccountView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.request.parser_context.get('kwargs')['user_id']
        if int(user_id) == self.request.user.pk:
            account = User.objects.get(id=user_id)
            account_serializer = AccountSerializer(account)
            return Response(account_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
