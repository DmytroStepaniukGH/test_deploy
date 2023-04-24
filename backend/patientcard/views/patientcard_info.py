from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from patientcard.serializers.patientcard_info import PatientCardInfoSerializer # noqa
from users.serializers import AppointmentSerializer # noqa
from patientcard.models import PatientCard # noqa
from users.models import Appointment # noqa


@extend_schema(
    tags=['Patient'],
    description="Return patient card by card ID"
)
class PatientCardInfoView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = PatientCardInfoSerializer

    def get(self, request, *args, **kwargs):
        card_id = self.request.parser_context.get('kwargs')['card_id']

        if self.request.user.pk:
            patient_card = PatientCard.objects.get(card_id=card_id)
            patient_card_serializer = PatientCardInfoSerializer(patient_card)
            return Response(patient_card_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
