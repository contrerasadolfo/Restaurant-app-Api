from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Crear un nuevo usuario con un correo electrónico de forma exitosa"""
        email = 'restaurant@test.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Normalizar el correo electrónico para un nuevo usuario"""
        email = 'test@GimaIl.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Prueba de validacion sin correo electrónico genera un error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
