from django.core.exceptions import ValidationError

from config import settings


def validate_phone_number(phone):
    if not(len(phone) == 12 and phone[0] == '+') and not(len(phone) == 11 and phone[0] == '8'):
        raise ValidationError('Некорректный ввод номера телефона.')


def validate_operator_code(code):
    if code in settings.INCORRECT_MOBILE_OPERATOR_CODES:
        raise ValidationError('Некорректный код мобильного оператора.')