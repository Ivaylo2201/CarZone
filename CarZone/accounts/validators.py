from django.core.exceptions import ValidationError


def validate_phone_number(value: str):
    if len(value) != 10:
        raise ValidationError('Phone number must be exactly 10 chars long!')
    if not value.startswith('0'):
        raise ValidationError('Phone number must start with a 0!')
