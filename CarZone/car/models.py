from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from .choices import BODY_TYPES, COLORS, TRANSMISSION_TYPES, FUEL_TYPES, EURO_STANDARD
from .validators import validate_manufacture_year

UserModel = get_user_model()


class Manufacturer(models.Model):
    NAME_MAX_LENGTH: int = 50

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    logo = models.ImageField(upload_to='manufacturers/')


class Feature(models.Model):
    NAME_MAX_LENGTH: int = 25

    name = models.CharField(max_length=NAME_MAX_LENGTH)


class Car(models.Model):
    BRAND_MAX_LENGTH: int = 25
    MODEL_MAX_LENGTH: int = 25
    MANUFACTURE_YEAR_MIN_VALUE: int = 2000
    TRANSMISSION_TYPE_MAX_LENGTH: int = 15
    POWER_MAX_VALUE: int = 1000
    CUBIC_CAPACITY_MAX_VALUE: int = 7500
    MILEAGE_MAX_VALUE: int = 750_000
    BODY_TYPE_MAX_LENGTH: int = 20
    FUEL_TYPE_MAX_LENGTH: int = 15
    COLOR_MAX_LENGTH: int = 15

    brand = models.CharField(
        max_length=BRAND_MAX_LENGTH
    )

    model = models.CharField(
        max_length=MODEL_MAX_LENGTH
    )

    manufacture_year = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MANUFACTURE_YEAR_MIN_VALUE),
            validate_manufacture_year
        )
    )

    transmission_type = models.CharField(
        max_length=TRANSMISSION_TYPE_MAX_LENGTH,
        choices=TRANSMISSION_TYPES,
    )

    horsepower = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(POWER_MAX_VALUE),)
    )

    capacity = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(CUBIC_CAPACITY_MAX_VALUE),)
    )

    euro_standard = models.PositiveSmallIntegerField(
        choices=EURO_STANDARD,
    )

    mileage = models.PositiveIntegerField(
        validators=(MaxValueValidator(MILEAGE_MAX_VALUE),)
    )

    body_type = models.CharField(
        max_length=BODY_TYPE_MAX_LENGTH,
        choices=BODY_TYPES,
    )

    fuel_type = models.CharField(
        max_length=FUEL_TYPE_MAX_LENGTH,
        choices=FUEL_TYPES,
    )

    color = models.CharField(
        max_length=COLOR_MAX_LENGTH,
        choices=COLORS,
    )

    price = models.PositiveIntegerField()

    views = models.PositiveSmallIntegerField(default=0, editable=False)

    dealer = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
    )

    manufacturer = models.ForeignKey(
        to=Manufacturer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cars'
    )

    features = models.ManyToManyField(to=Feature)
    warranty = models.PositiveSmallIntegerField()
    is_available = models.BooleanField(default=True, editable=False)

    @property
    def get_brand_model(self) -> str:
        return f'{self.brand} {self.model}'


class CarImage(models.Model):
    car = models.ForeignKey(to=Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
