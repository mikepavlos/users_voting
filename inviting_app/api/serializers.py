from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from profiles.models import Profile
from users.validators import phone_validator

User = get_user_model()

PROFILE_FIELDS = ('user_id', 'phone', 'invite_code', 'invitations')


class SignUpSerializer(serializers.Serializer):
    phone = serializers.IntegerField(
        required=True,
        validators=[phone_validator]
    )


class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    phone = serializers.ReadOnlyField(source='user.phone')
    invitations = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = PROFILE_FIELDS + ('activated_invite',)
        read_only_fields = PROFILE_FIELDS

    def get_invitations(self, obj):
        return (
            User.objects
            .filter(profile__activated_invite=obj.invite_code)
            .values_list('phone', flat=True)
        ) or None

    def validate_activated_invite(self, value):
        if self.instance.activated_invite:
            raise ValidationError(
                'В профиле уже активирован некий код.'
            )
        if value == self.instance.invite_code:
            raise ValidationError(
                'Нельзя активировать собственный код.'
            )
        if not Profile.objects.filter(invite_code=value).exists():
            raise ValidationError(
                f'Пользователь с кодом {value} не найден.'
            )
        return value
