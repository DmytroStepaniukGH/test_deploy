from django.urls import path
from .views import CreateAppointmentView, AppointmentListView, AvailableSlotsView, AllSpecializations, \
    DoctorsListViewSet, SearchAPIView, FilterDoctors, CancelAppointmentView, SetUnavailableTimeView, \
    CloseAppointmentView, DoctorView, MediaCreateRetrieve, ActiveAppointmentListView, ActiveAppointmentView, \
    ConfirmAppointmentView, UnconfirmedAppointmentListView

from reviews.views.reviews_doctor import DoctorReviewListView

urlpatterns = [
    path('appointments/', AppointmentListView.as_view(), name='appointments'),
    path('active-appointments/', ActiveAppointmentListView.as_view(), name='active-appointments'),
    path('unconfirmed-appointments/', UnconfirmedAppointmentListView.as_view(), name='unconfirmed-appointments'),
    path('active-appointments/appointment-<int:appointment_id>', ActiveAppointmentView.as_view(), name='active-appointment'),
    path('active-appointments/appointment-<int:appointment_id>/close', CloseAppointmentView.as_view(), name='close-appointment'),
    path('active-appointments/', ActiveAppointmentListView.as_view(), name='active-appointments'),
    path('available-slots/<int:doctor_id>/<str:date>', AvailableSlotsView.as_view(), name='available-slots'),
    path('new-appointment/<int:doctor_id>/<str:date>/<str:time>', CreateAppointmentView.as_view(), name='new-appointment'),
    path('confirm-appointment/<int:appointment_id>', ConfirmAppointmentView.as_view(), name='confirm-appointment'),
    path('cancel-appoitment/<int:appointment_id>', CancelAppointmentView.as_view(), name='cancel-appointment'),
    path('set-unavailable-time/<str:date>/<str:time>', SetUnavailableTimeView.as_view(), name='set-unavailable-time'),
    path('specializations/', AllSpecializations.as_view({'get': 'list'}), name='specializations'),
    path('doctors/', DoctorsListViewSet.as_view({'get': 'list'}), name='doctors'),
    path('doctors/doctor-<int:doctor_id>', DoctorView.as_view(), name='doctor'),
    path('doctors/doctor-<int:doctor_id>/reviews', DoctorReviewListView.as_view(), name='doctor-reviews'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('filter-doctors/<str:specialization>', FilterDoctors.as_view({'get': 'list'}), name='filter-doctors'),
    #path('doctor/change-photo/', MediaCreateRetrieve.as_view({'post': 'create'}), name='change-photo'),
]