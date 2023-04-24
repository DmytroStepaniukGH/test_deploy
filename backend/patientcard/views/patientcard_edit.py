from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from patientcard.serializers.patientcard_edit import PatientCardEditSerializer # noqa
from patientcard.models import PatientCard # noqa
from users.models import Patient # noqa


@extend_schema(
    tags=['Patient'],
    description="Edit patient card if user is doctor."
)
class PatientCardEditView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = PatientCardEditSerializer

    def update(self, request, *args, **kwargs):
        card_id = self.request.parser_context.get('kwargs')['card_id']
        partial = kwargs.pop('partial', False)
        queryset = PatientCard.objects.filter(card_id=card_id)
        patient_card_instance = get_object_or_404(queryset)
        serializer = PatientCardEditSerializer(patient_card_instance, data=request.data, partial=partial)

        if serializer.is_valid():
            if not self.request.user.is_doctor:
                return Response(
                    {"authorize": "You dont have permission for this user."},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)