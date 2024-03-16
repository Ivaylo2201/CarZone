from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import LOCATIONS
from .validators import validate_phone_number


class CarZoneUser(AbstractUser):
    LOCATION_MAX_LENGTH: int = 20
    PHONE_NUMBER_MAX_LENGTH: int = 10

    profile_picture = models.ImageField(
        upload_to='users/',
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        choices=LOCATIONS,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        validators=(validate_phone_number,),
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
