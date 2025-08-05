from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import CustomUserManager

User=get_user_model()

class CustomUserManagerTest(TestCase):
    def setUp(self):
        self.manager = CustomUserManager()
        self.manager.model=User

    def test_create_user_success(self):
        user=User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='testpass123'
            )

    def test_create_user_without_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='test@example.com',
                password=''
            )

    def test_create_superuser_success(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass',
            full_admin='Admin'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpass',
                is_staff=False
            )

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpass',
                is_superuser=False

            )