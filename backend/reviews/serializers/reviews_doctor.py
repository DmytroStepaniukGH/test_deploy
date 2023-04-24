from rest_framework import serializers

from reviews.models import Review # noqa


class DoctorReviewListSerializer(serializers.ModelSerializer):
    patient_lastname = serializers.CharField(source='appointment.patient.user.last_name')
    patient_firstname = serializers.CharField(source='appointment.patient.user.first_name')
    review_rating = serializers.CharField()
    review_text = serializers.CharField()

    class Meta:
        model = Review
        fields = (
            'patient_lastname',
            'patient_firstname',
            'review_rating',
            'review_text'
        )
