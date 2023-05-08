from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from reviews.models import Review
from reviews.serializers.reviews_doctor import DoctorReviewListSerializer


@extend_schema(
    tags=['Reviews'],
    description="Return reviews by doctor ID"
)
class DoctorReviewListView(ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = DoctorReviewListSerializer
    queryset = Review.objects.select_related('appointment', 'appointment__patient__user')

    def get_queryset(self):
        doctor_id = self.request.parser_context.get('kwargs')['doctor_id']
        queryset_filter = super().get_queryset().order_by('-created_at').filter(
            doctor_id=doctor_id
        )

        return queryset_filter
