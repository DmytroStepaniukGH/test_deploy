from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification # noqa
from notifications.serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    tags=['Notifications'],
    description="Return list of all notifications for authorized patient"
)
class NotificationsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.order_by('-id').all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(patient_id=self.request.user.patient)


@extend_schema(
    tags=['Notifications'],
    description="Return list of unread notifications for authorized patient"
)
class UnreadNotificationsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.order_by('-id').all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(patient_id=self.request.user.patient, is_read=False)


@extend_schema(
    tags=['Notifications'],
    description="Return number of unread notifications for authorized patient"
)
class CountUnreadNotificationsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        return Response({'count': Notification.objects.filter(patient_id=self.request.user.patient, is_read=False).count()},
                        status=status.HTTP_202_ACCEPTED)


@extend_schema(
    tags=['Notifications'],
    description="Toggle status notification"
)
class ToggleNotificationStatus(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def post(self, *args, **kwargs):
        notification_id = self.request.parser_context.get('kwargs')['notification_id']
        notification = Notification.objects.get(id=notification_id)
        current_status = notification.is_read
        notification.is_read = not current_status
        notification.save()

        return Response('Status of notification has been updated successfully',
                        status=status.HTTP_202_ACCEPTED)
