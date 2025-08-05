from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

from apps.users.services import (
    login_user_service,
    register_user_service,
    refresh_token_service,
    update_user_service,
    get_user_profile_service
)

User = get_user_model()


class LoginUserServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )

    @patch('apps.users.services.get_user_by_email_and_password')
    @patch('apps.users.services.UserProfileSerializer')
    def test_login_user_success(self, mock_serializer, mock_get_user):
        mock_get_user.return_value = self.user
        mock_serializer.return_value.data = {
            'user_id': str(self.user.user_id),
            'email': self.user.email,
            'full_name': self.user.full_name
        }

        data = {'email': self.user.email, 'password': 'testpass123'}
        result = login_user_service(data)

        self.assertIn('refresh', result)
        self.assertIn('access', result)
        self.assertIn('user', result)

    @patch('apps.users.services.get_user_by_email_and_password')
    def test_login_user_invalid_credentials(self, mock_get_user):
        mock_get_user.return_value = None
        with self.assertRaises(ValueError) as context:
            login_user_service({'email': 'wrong@example.com', 'password': 'wrong'})
        self.assertEqual(str(context.exception), "Invalid email or password")

    @patch('apps.users.services.get_user_by_email_and_password')
    def test_login_inactive_user(self, mock_get_user):
        user = User.objects.create_user(
            email='inactive@example.com',
            password='testpass123',
            full_name='Inactive',
            is_active=False
        )
        mock_get_user.return_value = user
        with self.assertRaises(ValueError) as context:
            login_user_service({'email': user.email, 'password': 'testpass123'})
        self.assertEqual(str(context.exception), "User is inactive")


class RegisterUserServiceTest(TestCase):
    @patch('apps.users.services.create_user_repo')
    @patch('apps.users.services.UserProfileSerializer')
    def test_register_user_success(self, mock_serializer, mock_create_user):
        user_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'full_name': 'New User'
        }

        mock_user = MagicMock()
        mock_create_user.return_value = mock_user
        mock_serializer.return_value.data = user_data

        result = register_user_service(user_data)

        mock_create_user.assert_called_once_with(**user_data)
        mock_serializer.assert_called_once_with(mock_user)
        self.assertEqual(result, user_data)


class RefreshTokenServiceTest(TestCase):
    def test_refresh_token_service(self):
        test_data = {'refresh': 'test_refresh_token'}
        result = refresh_token_service(test_data)
        self.assertEqual(result, test_data)


class UpdateUserServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            avatar='https://old-avatar.com/avatar.jpg'
        )

    @patch('apps.users.services.upload_to_supabase')
    @patch('apps.users.services.update_user_repo')
    @patch('apps.users.services.UserProfileSerializer')
    def test_update_user_with_avatar(self, mock_serializer, mock_update_repo, mock_upload):
        mock_file = MagicMock()
        mock_upload.return_value = 'https://new-avatar.com/avatar.jpg'
        mock_update_repo.return_value = self.user
        mock_serializer.return_value.data = {'email': 'test@example.com'}

        update_data = {
            'full_name': 'Updated Name',
            'avatar': mock_file
        }

        result = update_user_service(self.user, update_data)

        mock_upload.assert_called_once_with(
            file=mock_file,
            folder="avatars",
            previous_url=self.user.avatar
        )
        mock_update_repo.assert_called_once_with(
            self.user,
            {'full_name': 'Updated Name', 'avatar': 'https://new-avatar.com/avatar.jpg'}
        )

    @patch('apps.users.services.update_user_repo')
    @patch('apps.users.services.UserProfileSerializer')
    def test_update_user_without_avatar(self, mock_serializer, mock_update_repo):
        mock_update_repo.return_value = self.user
        mock_serializer.return_value.data = {'email': 'test@example.com'}

        update_data = {
            'full_name': 'Updated Name',
            'phone_number': '+1234567890'
        }

        result = update_user_service(self.user, update_data)
        mock_update_repo.assert_called_once_with(self.user, update_data)


class GetUserProfileServiceTest(TestCase):
    def test_get_user_profile_service(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )
        result = get_user_profile_service(user)
        self.assertEqual(result, user)
