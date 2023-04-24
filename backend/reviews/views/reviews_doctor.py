from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from reviews.models import Review # noqa
from reviews.serializers.reviews_doctor import DoctorReviewListSerializer # noqa


@extend_schema(
    tags=['Reviews'],
    description="Return reviews by doctor ID"
)
class DoctorReviewListView(ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = DoctorReviewListSerializer
    queryset = Review.objects.all()

    def get_queryset(self):
        doctor_id = self.request.parser_context.get('kwargs')['doctor_id']
        queryset_filter = super().get_queryset().filter(
            doctor_id=doctor_id
        )

        return queryset_filter


