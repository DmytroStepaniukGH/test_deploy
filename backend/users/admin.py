from django.contrib import admin
from .models import Patient, Doctor, Appointment, Specialization

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Specialization)
admin.site.register(Appointment)

