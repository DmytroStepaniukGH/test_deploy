from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from accounts.utils import decode_uid


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmPasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        user_model = get_user_model()
        uid = attrs['uid']
        token = attrs['token']

        try:
            user = user_model.objects.get(pk=decode_uid(uid))
        except (user_model.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'uid': _('Invalid uid')},
                code='invalid_uid',
            )

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {'token': _('Invalid token')},
                code='invalid_token',
            )

        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        user.set_password(validated_data['new_password'])
        user.save(update_fields=('password',))
        return user
