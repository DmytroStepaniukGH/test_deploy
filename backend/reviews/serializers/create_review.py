from rest_framework import serializers

from reviews.models import Review # noqa


class CreateReviewSerialiser(serializers.ModelSerializer):
    review_text = serializers.CharField(max_length=2000)
    review_rating = serializers.FloatField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = (
            'appointment_id',
            'doctor_id',
            'review_text',
            'review_rating'
        )

