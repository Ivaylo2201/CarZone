from django.core.exceptions import ValidationError


def validate_phone_number(value: str):
    if len(value) != 10:
        raise ValidationError('Invalid phone number length!')
    if not value.startswith('0'):
        raise ValidationError('Invalid phone number format!')
