from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from reviews.serializers.create_review import CreateReviewSerializer
from reviews.models import Review

from users.models import Appointment
from users.choises import StatusChoices


@extend_schema(
    tags=['Reviews'],
    description="Add review to appointment for authorized user"
)
class CreateReviewView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    serializer_class = CreateReviewSerializer

    def create(self, request, *args, **kwargs):
        appointment_id = self.request.parser_context.get('kwargs')['appointment_id']
        appointment = Appointment.objects.get(id=appointment_id)

        if appointment.status == StatusChoices.COMPLETED:
            try:
                review = Review.objects.get(appointment_id=appointment_id)
                return Response(status=status.HTTP_409_CONFLICT)

            except Review.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(
                    appointment_id=appointment_id,
                    doctor_id=appointment.doctor_id,
                )

            return Response(status=status.HTTP_200_OK)
        else:
            return Response('Appointment is active yet', status=status.HTTP_409_CONFLICT)
