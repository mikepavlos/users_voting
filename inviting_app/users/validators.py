import re

from django.core.exceptions import ValidationError


def phone_validator(value: str):
    if re.search(r'^\d{10}$', value) is None:
        raise ValidationError(
            'Некорректный телефонный номер. '
            'Введите номер телефона в виде 10-значного '
            'числа без первой цифры в формате <9991234567>.'
        )
    return value
