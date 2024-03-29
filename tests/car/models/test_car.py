from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

from CarZone.car.models import Car, Manufacturer
from CarZone.car.templatetags.car_tags import separate_digits, separate_thousands


class TestCar(TestCase):
    def setUp(self) -> None:
        self.car: Car = Car.objects.create(
            brand='Audi',
            model='RS7',
            manufacture_year=2024,
            transmission_type='Automatic',
            horsepower=250,
            capacity=3000,
            euro_standard=6,
            mileage=5000,
            body_type='Sedan',
            fuel_type='Diesel',
            color='Black',
            price=250000,
            warranty=12
        )


    def test_car_create_with_invalid_manufacture_year_should_raise_exception(self) -> None:
        current_year: int = datetime.now().year

        self.car.manufacture_year = current_year + 1

        with self.assertRaises(ValidationError) as ve:
            self.car.full_clean()

        expected: str = f'Ensure manufacture year does not exceed {current_year}!'
        actual: str = ve.exception.message_dict['manufacture_year'][0]

        self.assertEqual(expected, actual)


    def test_car_save_puts_correct_manufacturer_object(self) -> None:
        manufacturer: Manufacturer = Manufacturer.objects.create(name="Volkswagen")
        self.car.save()

        self.assertEqual(self.car.manufacturer.pk, manufacturer.pk)


    def test_car_save_puts_unknown_manufacturer_if_not_in_db(self) -> None:
        self.car.save()

        self.assertIsNone(self.car.manufacturer)


    def test_car__str__method(self) -> None:
        expected: str = 'Audi RS7'
        actual: str = str(self.car)

        self.assertEqual(expected, actual)


    def test_separate_digits_filter(self) -> None:
        phone_number: str = '0892350755'

        expected: str = '+359 892 350 755'
        actual: str = separate_digits(phone_number)

        self.assertEqual(expected, actual)


    def test_separate_thousands_filter(self) -> None:
        number: int = 1500000

        expected: str = '1 500 000'
        actual: str = separate_thousands(number)

        self.assertEqual(expected, actual)
