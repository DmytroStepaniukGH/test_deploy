from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    doctor_full_name = serializers.CharField(source='appointment.doctor.user.get_full_name')
    doctor_id = serializers.IntegerField(source='appointment.doctor.id')

    class Meta:
        model = Notification
        fields = (
            'id',
            'appointment',
            'doctor_id',
            'doctor_full_name',
            'title',
            'text',
            'is_read',
        )