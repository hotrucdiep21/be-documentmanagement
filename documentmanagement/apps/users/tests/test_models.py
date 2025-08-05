from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_creation_with_required_fields(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            full_name="Test_User"
        )
        self.assertIsInstance(user.user_id, uuid.UUID)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertIsNone(user.avatar)
        self.assertIsNone(user.phone_number)
        self.assertTrue(user.is_active)

    def test_user_str_method(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )
        self.assertEqual(str(user), 'test@example.com')

    def test_email_uniqueness(self):
        User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User 1'
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                password='testpass123',
                full_name='Test User 2'
            )

    def test_user_with_optional_fields(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            avatar='https://images.unsplash.com/photo-1590086782957-93c06ef21604?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2hpdGUlMjBndXl8ZW58MHx8MHx8fDA%3D',
            phone_number='0235635652'

        )
        self.assertEqual(
            user.avatar, 'https://images.unsplash.com/photo-1590086782957-93c06ef21604?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2hpdGUlMjBndXl8ZW58MHx8MHx8fDA%3D')
        self.assertEqual(user.phone_number, '1234234243')

    def test_username_field_configuration(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_required_fields_configuration(self):
        self.assertEqual(User.REQUIRED_FIELDS, ['full_name'])
