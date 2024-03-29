from django.test import TestCase

from CarZone.car.models import Feature

class TestFeature(TestCase):
    def test_feature__str__method(self) -> None:
        feature: Feature = Feature.objects.create(name='Feature')

        expected: str = 'Feature'
        actual: str = str(feature)

        self.assertEqual(expected, actual)