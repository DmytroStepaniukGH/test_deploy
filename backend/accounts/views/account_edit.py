from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from accounts.serializers.account_edit import AccountEditSerializer, AccountPasswordEditSerializer
from accounts.models import User


@extend_schema(
    tags=['Users'],
    description='Editing account page if user is patient.'
)
class AccountEditView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AccountEditSerializer

    def update(self, request, *args, **kwargs):
        user_id = self.request.parser_context.get('kwargs')['user_id']
        partial = kwargs.pop('partial', False)
        queryset = User.objects.filter(id=user_id)
        user_instance = get_object_or_404(queryset)
        serializer = AccountEditSerializer(user_instance, data=request.data, partial=partial)

        if serializer.is_valid():
            if user_id != self.request.user.pk:
                return Response(
                    {"authorize": "You dont have permission for this user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if self.request.user.is_doctor:
                return Response(
                    {"authorize": "Your personal data is not editable."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Users'],
    description='Editing password from account page.'
)
class AccountPasswordEditView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountPasswordEditSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, **kwargs})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
