from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

UserModel = get_user_model()


class TestUser(TestCase):
    def setUp(self) -> None:
        self.user: UserModel = UserModel.objects.create_user(
            username='username',
            password='password12345'
        )


    def test_user_create_with_invalid_phone_number_length_should_raise_exception(self) -> None:
        with self.assertRaises(ValidationError) as ve:
            self.user.phone_number = '089235075'
            self.user.full_clean()

        expected: str = 'Phone number must be exactly 10 chars long!'
        actual: str = ve.exception.message_dict['phone_number'][0]

        self.assertEqual(expected, actual)


    def test_user_create_with_invalid_phone_number_start_should_raise_exception(self) -> None:
        with self.assertRaises(ValidationError) as ve:
            self.user.phone_number = '1892350754'
            self.user.full_clean()

        expected: str = 'Phone number must start with a 0!'
        actual: str = ve.exception.message_dict['phone_number'][0]

        self.assertEqual(expected, actual)


    def test_user__str__method(self) -> None:
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'

        expected: str = 'John Doe'
        actual: str = str(self.user)

        self.assertEqual(expected, actual)
