from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager
from .validators import phone_validator


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя для авторизации.
    """

    phone = models.CharField(
        'Телефон',
        max_length=settings.PHONE_NUMBER_LENGTH,
        unique=True,
        validators=[phone_validator],
        help_text=(
            'Введите номер телефона в виде 10-тизначного '
            'числа без первой цифры в формате <9991234567>.'
        )
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.phone}'
