from django.core.exceptions import ValidationError
from datetime import datetime


def validate_manufacture_year(value: int) -> None:
    current_year: int = datetime.now().year

    if value > current_year:
        raise ValidationError(
            f'Ensure manufacture year does not exceed {current_year}!'
        )