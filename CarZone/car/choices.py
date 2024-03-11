from django.db import models


class TransmissionTypes(models.TextChoices):
    AUTOMATIC = 'Automatic', 'Automatic'
    MANUAL = 'Manual', 'Manual'


class BodyTypes(models.TextChoices):
    SEDAN = 'Sedan', 'Sedan'
    COUPE = 'Coupe', 'Coupe'
    WAGON = 'Wagon', 'Wagon'
    HATCHBACK = 'Hatchback', 'Hatchback'


class FuelTypes(models.TextChoices):
    BENSINE = 'Bensine', 'Bensine'
    DIESEL = 'Diesel', 'Diesel'
    GAS = 'Gas', 'Gas'
    ELECTRIC = 'Electric', 'Electric'


class Colors(models.TextChoices):
    WHITE = 'White', 'White'
    GREY = 'Grey', 'Grey'
    BLACK = 'Black', 'Black'
    RED = 'Red', 'Red'
    BLUE = 'Blue', 'Blue'
    YELLOW = 'Yellow', 'Yellow'
    ORANGE = 'Orange', 'Orange'
    GREEN = 'Green', 'Green'


EURO_STANDARD: tuple = (
    (1, 1), (2, 2), (3, 3),
    (4, 4), (5, 5), (6, 6)
)
