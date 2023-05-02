from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status, filters, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from drf_spectacular.utils import extend_schema

from users.models import Appointment, Doctor  # noqa
from users.serializers import AppointmentSerializer  # noqa


@extend_schema(
    tags=['Appointments'],
    description="Return list of finished appointments for authorized doctor/patient"
)
class FinishedAppointmentsListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    permission_classes = (IsAuthenticated,)
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
    description="Return filtered by specialization list of finished appointments for authorized patient"
)
class FilterFinishedAppointmentsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        specialization_id = self.request.parser_context.get('kwargs')['specialization_id']

        return super().get_queryset().filter(patient_id=self.request.user.patient,
                                             doctor__specialization__id=specialization_id,
                                             status='Завершений')

    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [TokenAuthentication, BasicAuthentication]
    # serializer_class = AppointmentSerializer
    #
    # def get_queryset(self):
    #     specialization_id = self.request.parser_context.get('kwargs')['specialization_id']
    #
    #     return super().get_queryset().filter(patient_id=self.request.user.patient,
    #                                          doctor__specialization__id=specialization_id,
    #                                          status='Завершений')

    # def get(self, request, *args, **kwargs):
    #     patient = self.request.user.patient
    #
    #     if patient:
    #         specialization_id = self.request.parser_context.get('kwargs')['specialization_id']
    #         appointments = Appointment.objects.order_by('-date').filter(patient=patient,
    #                                                                     doctor__specialization__id=specialization_id,
    #                                                                     status='Завершений')
    #         paginator = LimitOffsetPagination()
    #         result_page = paginator.paginate_queryset(appointments, request)
    #         serializer = AppointmentSerializer(result_page, many=True, context={'request': request})
    #         response = Response(serializer.data, status=status.HTTP_200_OK)
    #         return response

    # appointments_serializer = AppointmentSerializer(results, many=True)
    # return self.get_paginated_response(appointments_serializer.data)
    # return Response(appointments_serializer.data, status=status.HTTP_200_OK)
    #
    # else:
    #     return Response('Access denied: only patient can filter',
    #                     status=status.HTTP_403_FORBIDDEN)


@extend_schema(
    tags=['Appointments'],
    description="Returns a list of finished visits for any patient"
)
class PatientFinishedAppointmentsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.all().prefetch_related('doctor').prefetch_related('patient')
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            patient_id = self.request.parser_context.get('kwargs')['patient_id']

            return super().get_queryset().order_by('-date').filter(patient_id=patient_id,
                                                                   status='Завершений')


@extend_schema(
    tags=['Appointments'],
    description="Returns the specialty-filtered list of finished visits for any patient"
)
class FilterPatientFinishedAppointmentsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.all().prefetch_related('patient').prefetch_related('doctor')
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            patient_id = self.request.parser_context.get('kwargs')['patient_id']
            specialization_id = self.request.parser_context.get('kwargs')['specialization_id']

            return super().get_queryset().order_by('-date').filter(patient_id=patient_id,
                                                                   doctor__specialization__id=specialization_id,
                                                                   status='Завершений')


@extend_schema(
    tags=['Appointments'],
    description="Return single appointment for authorized doctor/patient"
)
class FinishedAppointmentView(APIView):
    queryset = Appointment.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AppointmentSerializer

    def get(self, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        appointment_info = Appointment.objects.get(id=appointment_id)
        appointment_serializer = AppointmentSerializer(appointment_info)

        return Response(appointment_serializer.data, status=status.HTTP_200_OK)
