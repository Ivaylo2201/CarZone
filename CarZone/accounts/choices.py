from django.db import models


class Locations(models.TextChoices):
    BURGAS = 'Burgas', 'Burgas'
    DOBRICH = 'Dobrich', 'Dobrich'
    PLEVEN = 'Pleven', 'Pleven'
    PLOVDIV = 'Plovdiv', 'Plovdiv'
    RAZGRAD = 'Razgrad', 'Razgrad'
    RUSE = 'Ruse', 'Ruse'
    SLIVEN = 'Sliven', 'Sliven'
    SOFIA = 'Sofia', 'Sofia'
    TARGOVISHTE = 'Targovishte', 'Targovishte'
    VARNA = 'Varna', 'Varna'
    VELIKO_TARNOVO = 'Veliko Tarnovo', 'Veliko Tarnovo'
    VIDIN = 'Vidin', 'Vidin'
