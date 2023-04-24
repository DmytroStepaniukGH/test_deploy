from rest_framework import serializers

from accounts.models import User # noqa


class AccountSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    patronim_name = serializers.CharField(max_length=150)
    birth_date = serializers.CharField(max_length=8)
    sex = serializers.CharField()
    email = serializers.EmailField()
    phone_num = serializers.CharField(max_length=13)
    address_city = serializers.CharField(max_length=50)
    address_street = serializers.CharField(max_length=150)
    address_house = serializers.CharField(max_length=10)
    address_appartment = serializers.CharField(max_length=10)
    card_id = serializers.CharField(source='patient.card.card_id')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronim_name',
            'birth_date',
            'sex'
            'email',
            'phone_num'
            'address_city',
            'address_street',
            'address_house',
            'address_appartment',
            'card_id',
        )

