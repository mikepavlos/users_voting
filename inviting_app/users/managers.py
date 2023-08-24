from django.contrib.auth.models import UserManager as DjangoUserManager
from django.utils.crypto import get_random_string


class UserManager(DjangoUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Создание пользователя по номеру телефона."""

        if not phone:
            raise ValueError('Необходим номер телефона.')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(phone, password, **extra_fields)
        return user
