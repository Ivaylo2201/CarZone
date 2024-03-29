from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from CarZone.car.models import Car

UserModel = get_user_model()


class TestCar(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(username='username', password='password12345')
        self.client = Client()
        self.client.login(username='username', password='password12345')
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


    def test_car_remove_confirmation_page(self) -> None:
        response = self.client.get(reverse('car-remove-confirm', kwargs={'pk': self.car.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/remove-confirm.html')


    def test_car_remove_view(self) -> None:
        response = self.client.get(reverse('car-remove', kwargs={'pk': self.car.pk}))
        self.car.refresh_from_db()
        self.assertFalse(self.car.is_available)
        self.assertEqual(response.status_code, 302)
