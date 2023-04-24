from django.urls import path

from patientcard.views.patientcard_info import PatientCardInfoView # noqa
from patientcard.views.patientcard_edit import PatientCardEditView # noqa

urlpatterns = [
    path('patient-card/<int:card_id>', PatientCardInfoView.as_view(), name='patient-card'),
    path('patient-card-<int:card_id>/edit', PatientCardEditView.as_view(), name='patient-card-edit'),
]
