from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import Locations
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
        choices=Locations.choices
    )
    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        validators=(validate_phone_number,)
    )
