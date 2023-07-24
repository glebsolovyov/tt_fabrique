from typing import Optional

from django.core.exceptions import ValidationError

from core.configs.api import INCORRECT_MOBILE_OPERATOR_CODES


def validate_phone_number(phone: Optional[str]) -> None:
    """

    :param phone:
    """
    if not(len(phone) == 12 and phone[0] == '+') and not(len(phone) == 11 and phone[0] == '8'):
        raise ValidationError('Некорректный ввод номера телефона.')


def validate_operator_code(code: Optional[str]) -> None:
    """

    :param code:
    """
    if code in INCORRECT_MOBILE_OPERATOR_CODES:
        raise ValidationError('Некорректный код мобильного оператора.')