from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from drf_spectacular.utils import extend_schema

from users.models import Appointment, Doctor # noqa
from users.serializers import AppointmentSerializer # noqa


@extend_schema(
    tags=['Appointments'],
    description="Return list of finished appointments for authorized doctor/patient"
)
class FinishedAppointmentsListView(ListAPIView):
    queryset = Appointment.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        visit_status = 'Завершений'
        if not self.request.user.is_doctor:
            return super().get_queryset().filter(
                patient_id=self.request.user.patient,
                status=visit_status)

        else:
            return super().get_queryset().filter(
                doctor_id=self.request.user.doctor,
                status=visit_status)


@extend_schema(
    tags=['Appointments'],
    description="Returns a list of finished visits for any patient"
)
class PatientFinishedAppointmentsListView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AppointmentSerializer

    def get(self, *args, **kwargs):
        if self.request.user.is_doctor:
            patient_id = self.request.parser_context.get('kwargs')['patient_id']
            appointments = Appointment.objects.order_by('-date').filter(patient=patient_id, status='Завершений')
            appointments_serializer = AppointmentSerializer(appointments, many=True)

            return Response(appointments_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('Access denied: only doctor can view history of visits of patient',
                            status=status.HTTP_403_FORBIDDEN)


@extend_schema(
    tags=['Appointments'],
    description="Return single appointment for authorized doctor/patient"
)
class FinishedAppointmentView(APIView):
    queryset = Appointment.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AppointmentSerializer

    def get(self, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        appointment_info = Appointment.objects.get(id=appointment_id)
        appointment_serializer = AppointmentSerializer(appointment_info)

        return Response(appointment_serializer.data, status=status.HTTP_200_OK)
