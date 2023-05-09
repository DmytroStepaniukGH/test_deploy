from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from accounts.models import User


class AccountEditSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    patronim_name = serializers.CharField(max_length=150)
    birth_date = serializers.CharField(max_length=10)
    sex = serializers.CharField()
    email = serializers.EmailField()
    phone_num = serializers.CharField(max_length=13)
    address_city = serializers.CharField(max_length=50)
    address_street = serializers.CharField(max_length=150)
    address_house = serializers.CharField(max_length=10)
    address_appartment = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronim_name',
            'birth_date',
            'sex',
            'email',
            'phone_num',
            'address_city',
            'address_street',
            'address_house',
            'address_appartment'
        )


class AccountPasswordEditSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            'old_password',
            'password',
            'password2',
            'user_id'
        )

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user

        if user.pk != self.validated_data['user_id']:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        user.set_password(self.validated_data['password'])
        user.save()

        return user
