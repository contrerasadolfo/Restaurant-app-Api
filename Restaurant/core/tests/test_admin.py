from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='123345678'
        )
        # iniciar sesion como admin
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='12345678',
            nombre='Restaurant',
            apellido='Merida'
        )
    
    def test_users_listed(self):
        """Probar que los usuarios figuren en la página del usuario"""
        # {{ app_label }}_{{ model_name }}_changelist
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.nombre)
        self.assertContains(res, self.user.email)
    
    def test_user_chage_page(self):
        """Probar que la página de edición del usuario funcione"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Prueba para que la página de crear usuario"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
