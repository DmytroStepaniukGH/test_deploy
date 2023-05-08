from datetime import datetime

from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce

from drf_spectacular.utils import extend_schema

from rest_framework import generics, status, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Appointment, Doctor, Patient, Specialization
from users.serializers import AppointmentSerializer, DoctorListSerializer, SpecializationsSerializer, \
    SetUnavailableTimeSerializer, CreateAppointmentSerializer, CloseAppointmentSerializer
from users.models import check_date_time
from users.choises import StatusChoices

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

    queryset = Appointment.objects.select_related('doctor__specialization',
                                                  'doctor__user',
                                                  'patient__card',
                                                  'patient__user')

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            return super().get_queryset().filter(doctor_id=self.request.user.doctor.id,
                                                 status=StatusChoices.ACTIVE)

        return super().get_queryset().filter(patient_id=self.request.user.patient.id,
                                             status=StatusChoices.ACTIVE)


@extend_schema(
    tags=['Appointments'],
    description="Returns the specialty-filtered list of active appointments for authorized patient"
)
class FilterActiveAppointmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.select_related('patient__card',
                                                  'patient__user',
                                                  'doctor__specialization',
                                                  'doctor__user')

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        specialization_id = self.request.parser_context.get('kwargs')['specialization_id']

        return super().get_queryset().filter(patient_id=self.request.user.patient,
                                             doctor__specialization__id=specialization_id,
                                             status=StatusChoices.ACTIVE)


@extend_schema(
    tags=['Appointments'],
    description="Returns list of unconfirmed appointments for doctor"
)
class UnconfirmedAppointmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Appointment.objects.select_related('patient__card',
                                                  'patient__user',
                                                  'doctor__specialization',
                                                  'doctor__user')

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            return super().get_queryset().filter(doctor_id=self.request.user.doctor,
                                                 status=StatusChoices.UNCONFIRMED)


@extend_schema(
    tags=['Appointments'],
    description="Returns single active appointment for authorized user"
)
class ActiveAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer

    def get(self, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']

        appointment = Appointment.objects.select_related('patient__card',
                                                         'patient__user',
                                                         'doctor__specialization',
                                                         'doctor__user').get(id=appointment_id)

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
    queryset = Appointment.objects.select_related('patient')
    serializer_class = CloseAppointmentSerializer

    def patch(self, request, *args, **kwargs):
        doctor = self.request.user.doctor
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        medical_history = self.request.data.get('medical_history')
        objective_status = self.request.data.get('objective_status')
        diagnosis = self.request.data.get('diagnosis')
        examination = self.request.data.get('examination')
        recommendations = self.request.data.get('recommendations')

        appointment = self.get_queryset().filter(id=appointment_id)

        if appointment:
            if appointment.update(status=StatusChoices.COMPLETED, medical_history=medical_history,
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
            return Response({'Error': 'Doctor ID and date are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            doctor = Doctor.objects.get(id=doctor_id)

        except Doctor.DoesNotExist:
            return Response({'Error': f'Doctor with ID {doctor_id} does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)

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

        check_another_appointment = Appointment.objects.filter(patient=patient, date=date, time=time)

        if check_date_time(date, time):
            doctor = Doctor.objects.get(id=doctor_id)
            unavailable_times = doctor.unavailable_time.filter(date=date).values_list('time', flat=True)

            if not check_another_appointment:
                if time not in unavailable_times:
                    patient.create_appointment(doctor=doctor, date=date, time=time)
                    return Response(f'Appointment at {date} {time} has been created successfully',
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(f'Error: time {time} on {date} has been marked by doctor as unavailable',
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f'Error: you already have another appointment at {time} on {date} to'
                                f' {check_another_appointment.doctor.user.get_full_name()}',
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response('Date/time not valid', status=status.HTTP_400_BAD_REQUEST)


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
            if appointment.status == StatusChoices.UNCONFIRMED:
                if user.is_doctor:
                    appointment.status = StatusChoices.ACTIVE
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


"""
DOCTORS
"""


@extend_schema(
    tags=['Doctors'],
    description="Set unavailable time in doctor's schedule",
)
class SetUnavailableTimeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SetUnavailableTimeSerializer

    def post(self, *args, **kwargs):
        date = self.request.parser_context.get('kwargs')['date']
        time = self.request.parser_context.get('kwargs')['time']

        if check_date_time(date, time):
            doctor = Doctor.objects.get(user=self.request.user)
            doctor.set_unavailable_time(date, time)

            return Response(f'Time {date} {time} has been set unavailable',
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid date/time (you cannot set the time '
                                      'earlier than the current time) or format. '
                                      'Date/time must be in YYYY-MM-DD and HH:MM format'},
                            status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Doctors'],
    description="Search by specialization or doctor's last name",
)
class SearchAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    search_fields = ['user__last_name', 'specialization__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Doctor.objects.all().select_related('user', 'specialization').annotate(
        rating=Coalesce(Avg('reviews__review_rating'), Value(0), output_field=FloatField()))

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

    queryset = Doctor.objects.select_related('user', 'specialization').annotate(
        rating=Coalesce(Avg('reviews__review_rating'), Value(0), output_field=FloatField()))


@extend_schema(
    tags=['Doctors'],
    description="Return information about doctor"
)
class DoctorView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = DoctorListSerializer

    def get(self, request, *args, **kwargs):
        doctor_id = self.request.parser_context.get('kwargs')['doctor_id']

        doctor_info = Doctor.objects.select_related('user', 'specialization').annotate(
            rating=Coalesce(Avg('reviews__review_rating'), Value(0),
                            output_field=FloatField())).get(id=doctor_id)

        doctor_serializer = DoctorListSerializer(doctor_info, context={'request': request})

        return Response(doctor_serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Doctors'],
    description="Return list of all doctors filtered by specialization"
)
class FilterDoctors(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Doctor.objects.select_related('user', 'specialization').annotate(
            rating=Coalesce(Avg('reviews__review_rating'), Value(0), output_field=FloatField()))

    serializer_class = DoctorListSerializer

    def get_queryset(self, *args, **kwargs):
        specialization_id = self.request.parser_context.get('kwargs')['specialization_id']

        return self.queryset.filter(specialization_id=specialization_id)
