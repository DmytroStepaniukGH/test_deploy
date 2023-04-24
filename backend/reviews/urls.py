from django.urls import path

from reviews.views.finished_visites import FinishedAppointmentsListView, PatientFinishedAppointmentsListView  # noqa
from reviews.views.finished_visites import FinishedAppointmentView # noqa
from reviews.views.create_review import CreateReviewView # noqa
from reviews.views.create_pdf_visit_result import CreatePdfVisitResults # noqa

urlpatterns = [
    path('finished/', FinishedAppointmentsListView.as_view(), name='finished-appointments'),
    path('patient-finished/<int:patient_id>', PatientFinishedAppointmentsListView.as_view(), name='patient-finished-appointments'),
    path('finished/id-<int:appointment_id>', FinishedAppointmentView.as_view(), name='appointment'),
    path('finished/id-<int:appointment_id>/add-review', CreateReviewView.as_view(), name='add-review'),
    path('finished/id-<int:appointment_id>/create-pdf', CreatePdfVisitResults.as_view(), name='create-pdf')
]
