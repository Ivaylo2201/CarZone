from django.test import TestCase

from CarZone.car.models import Manufacturer

class TestManufacturer(TestCase):
    def test_manufacturer__str__method_when_there_is_no_country(self) -> None:
        manufacturer: Manufacturer = Manufacturer.objects.create(name='Name', country=None)

        expected: str = 'Name (?)'
        actual: str = str(manufacturer)

        self.assertEqual(expected, actual)


    def test_manufacturer__str__method_when_there_is_a_country(self) -> None:
        manufacturer: Manufacturer = Manufacturer.objects.create(name='Name', country='Country')

        expected: str = 'Name (Country)'
        actual: str = str(manufacturer)

        self.assertEqual(expected, actual)