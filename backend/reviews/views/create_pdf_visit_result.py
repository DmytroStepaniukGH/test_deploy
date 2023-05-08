import io

from django.http import FileResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from drf_spectacular.utils import extend_schema

from users.models import Appointment
from users.serializers import AppointmentSerializer


@extend_schema(
    tags=['Appointments'],
    description='Create PDF file for finished appointment result by appointment ID'
)
class CreatePdfVisitResults(GenericAPIView):
    queryset = Appointment.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AppointmentSerializer

    def get(self, request, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        appointment_info = Appointment.objects.select_related('patient__user',
                                                              'patient__card',
                                                              'doctor__user',
                                                              'doctor__specialization').get(id=appointment_id)

        appointment_serializer = AppointmentSerializer(appointment_info)
        appointment_data = appointment_serializer.data

        filename = f'{appointment_info.patient} - {appointment_info.doctor.user.get_full_name()}.pdf'

        buffer = io.BytesIO()
        pdf_object = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('Times New Roman', 'Times.ttf'))
        pdf_object.setFont('Times New Roman', 12)

        pdf_object.drawString(30, 750, 'Пацієнт: '+str(appointment_info.patient))
        pdf_object.drawString(30, 730, 'Лікар: '+str(appointment_info.doctor))
        pdf_object.drawString(30, 710, 'Дата візиту: '+str(appointment_info.date)+' '+str(appointment_info.time))

        medical_history = pdf_object.beginText(30, 690)
        medical_history.textLines(
            'Анамнез захворювання: '+str(appointment_data['medical_history'].replace('. ', '.\n'))
        )
        pdf_object.drawText(medical_history)

        objective_status = pdf_object.beginText(30, 650)
        objective_status.textLines(
            'Обʼєктивний статус: '+str(appointment_data['objective_status']).replace('. ', '.\n')
        )
        pdf_object.drawText(objective_status)

        pdf_object.drawString(30, 500, 'Діагноз: '+str(appointment_data['diagnosis']))

        examination = pdf_object.beginText(30, 480)
        examination.textLines('Обстеження: '+str(appointment_data['examination']))
        pdf_object.drawText(examination)

        recommendations = pdf_object.beginText(30, 460)
        recommendations.textLines('Рекомендації: '+str(appointment_data['recommendations']).replace('. ', '.\n'))
        pdf_object.drawText(recommendations)

        pdf_object.showPage()
        pdf_object.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=filename)
