from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets, filters
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Appointment, Doctor, Patient, Specialization, Media
from .serializers import AppointmentSerializer, DoctorListSerializer, SpecializationsSerializer, \
    SetUnavailableTimeSerializer, CreateAppointmentSerializer, MediaSerializer, CloseAppointmentSerializer
from notifications.models import Notification


"""
APPOINTMENTS
"""


@extend_schema(
    tags=['Appointments'],
    description="Returns list of appointments for authorized user"
)
class AppointmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            return super().get_queryset().filter(doctor_id=self.request.user.doctor)

        return super().get_queryset().filter(patient_id=self.request.user.patient)


@extend_schema(
    tags=['Appointments'],
    description="Returns list of active appointments for authorized user"
)
class ActiveAppointmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Appointment.objects.all().select_related('patient__card').\
        select_related('doctor__specialization').\
        select_related('patient__user').select_related('doctor__user')

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            return super().get_queryset().filter(doctor_id=self.request.user.doctor, status='Активний')

        return super().get_queryset().filter(patient_id=self.request.user.patient, status='Активний')


@extend_schema(
    tags=['Appointments'],
    description="Returns the specialty-filtered list of active appointments for authorized patient"
)
class FilterActiveAppointmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.all().select_related('patient__card').\
        select_related('doctor__specialization').\
        select_related('patient__user').select_related('doctor__user')

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        specialization_id = self.request.parser_context.get('kwargs')['specialization_id']

        return super().get_queryset().filter(patient_id=self.request.user.patient,
                                             doctor__specialization__id=specialization_id,
                                             status='Активний')


@extend_schema(
    tags=['Appointments'],
    description="Returns list of unconfirmed appointments for doctor"
)
class UnconfirmedAppointmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Appointment.objects.all().select_related('patient__card').\
        select_related('doctor__specialization').\
        select_related('patient__user').select_related('doctor__user')

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            return super().get_queryset().filter(doctor_id=self.request.user.doctor, status='Непідтверджений')


@extend_schema(
    tags=['Appointments'],
    description="Returns single active appointment for authorized user"
)
class ActiveAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer

    def get(self, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']

        appointment = Appointment.objects.get(id=appointment_id)

        if appointment:
            appointment_serializer = AppointmentSerializer(appointment)
            return Response(appointment_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Invalid appointment id', status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Appointments'],
    description="Close appointment by doctor"
)
class CloseAppointmentView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.all()
    serializer_class = CloseAppointmentSerializer

    def put(self, request, *args, **kwargs):
        doctor = self.request.user.doctor
        # new_status = self.request.data.get('status')
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        medical_history = self.request.data.get('medical_history')
        objective_status = self.request.data.get('objective_status')
        diagnosis = self.request.data.get('diagnosis')
        examination = self.request.data.get('examination')
        recommendations = self.request.data.get('recommendations')

        appointment = self.get_queryset().filter(id=appointment_id)

        if appointment:
            if appointment.update(status='Завершений', medical_history=medical_history,
                                  objective_status=objective_status, diagnosis=diagnosis,
                                  examination=examination, recommendations=recommendations):

                notification = Notification(appointment=appointment[0],
                                            patient=appointment[0].patient, title='Оцініть ваш візит',
                                            text=f'Дякуємо за візит до нашої поліклініки! '
                                                 f'Будь ласка, оцініть ваш візит до лікаря '
                                                 f'{doctor.user.get_full_name()} {appointment[0].date}'
                                                 f' о {appointment[0].time}')

                notification.save()

                return Response('Appointment has been updated successfully', status=status.HTTP_202_ACCEPTED)
            return Response('Error: please, check your data', status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response('Error: appointment does not exists', status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=['Appointments'],
    description="Return list of available slots of doctor"
)
class AvailableSlotsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        doctor_id = self.request.parser_context.get('kwargs')['doctor_id']
        date_str = self.request.parser_context.get('kwargs')['date']
        if not doctor_id or not date_str:
            return Response({'Error': 'Doctor ID and date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            doctor = Doctor.objects.get(id=doctor_id)

        except Doctor.DoesNotExist:
            return Response({'Error': f'Doctor with ID {doctor_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

        except ValueError:
            return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'},
                            status=status.HTTP_400_BAD_REQUEST)

        available_slots = doctor.get_available_slots(date)

        return Response(available_slots, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Appointments'],
    description="Create a new appointment by authorized patient"
)
class CreateAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateAppointmentSerializer

    def post(self, request, *args, **kwargs):
        date = self.request.parser_context.get('kwargs')['date']
        time = self.request.parser_context.get('kwargs')['time']
        doctor_id = self.request.parser_context.get('kwargs')['doctor_id']

        patient = Patient.objects.get(user=self.request.user)

        return Response(patient.create_appointment(doctor_id=doctor_id, date=date, time=time))


@extend_schema(
    tags=['Appointments'],
    description="Confirm appointment by doctor"
)
class ConfirmAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer

    def patch(self, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        user = self.request.user
        appointment = Appointment.objects.get(id=appointment_id)

        if appointment:
            if appointment.status == "Непідтверджений":
                if user.is_doctor:
                    appointment.status = 'Активний'
                    appointment.save()
                    return Response(f'Appointment confirmed successfully', status=status.HTTP_200_OK)
                else:
                    return Response(f'Only doctor can confirm the appointment', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f'Only unconfirmed appointment can be confirm', status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(f'No records found with this id',
                            status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Appointments'],
    description="Cancel appointment by authorized patient/doctor"
)
class CancelAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer

    def delete(self, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        user = self.request.user
        appointment = Appointment.objects.get(id=appointment_id)

        if appointment:
            if not user.is_doctor:
                appointment.delete()
                return Response(f'Appointment canceled by patient', status=status.HTTP_200_OK)
            else:
                appointment.delete()
                return Response(f'Appointment canceled by doctor', status=status.HTTP_200_OK)
        else:
            return Response(f'No records found with this id',
                            status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Doctors']
)
class SetUnavailableTimeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SetUnavailableTimeSerializer

    def post(self, *args, **kwargs):
        date_to_set_unavailable = self.request.parser_context.get('kwargs')['date']
        time_to_set_unavailable = self.request.parser_context.get('kwargs')['time']

        if not date_to_set_unavailable or not time_to_set_unavailable:
            return Response({'Error': 'Date and time are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date_to_cancel = datetime.strptime(date_to_set_unavailable, '%Y-%m-%d').date()

        except ValueError:
            return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'},
                            status=status.HTTP_400_BAD_REQUEST)

        doctor = Doctor.objects.get(user=self.request.user)
        doctor.set_unavailable_time(date_to_set_unavailable, time_to_set_unavailable)

        return Response(f'Time {date_to_cancel} {time_to_set_unavailable} has been set unavailable',
                        status=status.HTTP_200_OK)


@extend_schema(
    tags=['Doctors'],
    description="Search by specialization or doctor's last name",
)
class SearchAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    search_fields = ['user__last_name', 'specialization__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Doctor.objects.all().select_related('user').select_related('specialization')
    serializer_class = DoctorListSerializer


@extend_schema(
    tags=['Doctors'],
    description='Returns list of all specializations'
)
class AllSpecializations(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SpecializationsSerializer
    queryset = Specialization.objects.order_by('name').all()


@extend_schema(
    tags=['Doctors'],
    description='Returns list of all doctors'
)
class DoctorsListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = DoctorListSerializer

    queryset = Doctor.objects.all().select_related('specialization').select_related('user')


@extend_schema(
    tags=['Doctors'],
    description="Return information about doctor"
)
class DoctorView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = DoctorListSerializer

    def get(self, *args, **kwargs):
        doctor_id = self.request.parser_context.get('kwargs')['doctor_id']

        doctor_info = Doctor.objects.select_related('user').select_related('specialization').get(id=doctor_id)
        doctor_serializer = DoctorListSerializer(doctor_info)

        return Response(doctor_serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Doctors'],
    description="Return list of all doctors filtered by specialization"

)
class FilterDoctors(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    model = Doctor
    serializer_class = DoctorListSerializer

    def get_queryset(self, *args, **kwargs):
        specialization_id = self.request.parser_context.get('kwargs')['specialization_id']

        queryset = Doctor.objects.filter(specialization_id=specialization_id).\
            select_related('user').select_related('specialization')

        return queryset


class MediaCreateRetrieve(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaSerializer
    parser_classes = (MultiPartParser,)
    queryset = Media.objects.select_related('created_by').all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.doctor)
