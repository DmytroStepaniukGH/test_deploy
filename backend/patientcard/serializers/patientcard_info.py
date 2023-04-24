from rest_framework import serializers

from patientcard.models import PatientCard # noqa
from accounts.models import User # noqa
from users.models import Appointment # noqa


class PatientCardInfoSerializer(serializers.Serializer):
    card_id = serializers.IntegerField()
    patient = serializers.CharField()
    birth_date = serializers.CharField(source='patient.user.birth_date')
    sex = serializers.CharField(source='patient.user.sex')
    email = serializers.CharField(source='patient.user.email')
    phone_num = serializers.CharField(source='patient.user.phone_num')
    address = serializers.CharField(source='patient.user.get_full_address')

    register_date = serializers.DateField()
    blood_group = serializers.CharField()
    traumas_info = serializers.CharField()
    operations_info = serializers.CharField()
    chronical_illness_info = serializers.CharField()

    class Meta:
        model = PatientCard
        fields = (
            'card_id',
            'patient',
            'birth_date',
            'sex',
            'email',
            'phone_num',
            'address',
            'register_date',
            'blood_group',
            'traumas_info',
            'operations_info',
            'chronical_illness_info'
        )
