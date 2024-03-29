from django.contrib.auth import get_user_model
from django.test import TestCase, Client

UserModel = get_user_model()


class TestUser(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(username='username', password='password12345')
        self.client = Client()


    def test_initial(self) -> None:
        self.client.login(username='username', password='password12345')

        response = self.client.get('http://localhost:8000/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/car/catalogue/')
