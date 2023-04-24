from rest_framework import serializers

from patientcard.models import PatientCard # noqa
from accounts.models import User # noqa
from users.models import Appointment # noqa


class PatientCardEditSerializer(serializers.Serializer):
    traumas_info = serializers.CharField()
    operations_info = serializers.CharField()
    chronical_illness_info = serializers.CharField()

    class Meta:
        model = PatientCard,
        fields = (
            'traumas_info',
            'operations_info',
            'chronical_illness_info'
        )

    def update(self, instance, validated_data):
        for key in validated_data:
            setattr(instance, key, validated_data[key])

        instance.save()

        return instance