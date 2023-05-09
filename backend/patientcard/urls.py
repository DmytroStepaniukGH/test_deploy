from django.urls import path

from patientcard.views.patientcard_info import PatientCardInfoView
from patientcard.views.patientcard_edit import PatientCardEditView

urlpatterns = [
    path('patient-card/<int:card_id>', PatientCardInfoView.as_view(), name='patient-card'),
    path('patient-card-<int:card_id>/edit', PatientCardEditView.as_view(), name='patient-card-edit'),
]
