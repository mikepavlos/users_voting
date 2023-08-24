from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.validators import phone_validator

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    phone = serializers.IntegerField(
        required=True,
        validators=[phone_validator]
    )


class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    invite_code = serializers.ReadOnlyField(source='profile.invite_code')
    activated_invite = serializers.ReadOnlyField(
        source='profile.activated_invite'
    )

    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'profile_id',
            'invite_code',
            'activated_invite'
        )
        read_only_fields = fields


class InviteSerializer(serializers.Serializer):
    activated_invite = serializers.CharField(
        max_length=settings.INVITE_CODE_LENGTH,
        min_length=settings.INVITE_CODE_LENGTH,
        required=True
    )
