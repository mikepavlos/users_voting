from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    """
    Модель профиля пользователя.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='Пользователь',
    )
    invite_code = models.CharField(
        'Инвайт код',
        max_length=settings.INVITE_CODE_LENGTH,
        unique=True,
    )
    activated_invite = models.CharField(
        'Активированный код другого участника',
        max_length=settings.INVITE_CODE_LENGTH,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(activated_invite=models.F('invite_code')),
                name='self_invite'
            ),
        ]

    def __str__(self):
        return f'{self.user}'
