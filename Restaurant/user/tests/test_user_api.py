from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApi(TestCase):
    """Prueba para el API publica de users"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Prueba para crear usuario con exito"""
        payload = {
            'email': 'restaurant@test.com',
            'password': 'restaurant',
            'nombre': 'rest',
            'apellido': 'Sojo',
            'direccion': 'Merida'

        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # comprobacion de que el usuario se creo
        user= get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

        # comprobar que la clave no sea devuelta como parte del obj
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        """Prueba para un usuario que exista en BD"""
        payload = {'email': 'rest@test.com', 'password': 'passRest'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Prueba para restringir longitud de password"""
        payload = {'email': 'rest@test.com', 'password': 'ps'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Prueba para generar un token"""
        payload = {'email': 'rest@test.com', 'password': 'restaurante'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Prueba no crear token con credencials invalidas"""
        create_user(email='rest@test.com', password='test123' )
        payload = {'email': 'rest@test.com', 'password': 'restaurante'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_not_user(self):
        """Prueba no crear token si el usuario no existe"""

        payload = {'email': 'rest@test.com', 'password': 'restaurante'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Prueba no crear token sin el campo Email o Password"""
        res = self.client.post(TOKEN_URL, {'email': 'restaurant', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)










