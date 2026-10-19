from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_default_recruiter_login_provisions_and_authenticates(self):
        """Ensure standard recruiter credentials auto-provision lead recruiter account."""
        response = self.client.post('/api/auth/login/', {
            'username': 'recruiter',
            'password': 'recruitiq2026',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['role'], 'RECRUITER')

    def test_login_with_token_alias(self):
        """Ensure /api/auth/token/ alias also works."""
        response = self.client.post('/api/auth/token/', {
            'username': 'recruiter',
            'password': 'recruitiq2026',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_credentials_rejected(self):
        """Ensure invalid password returns 401 Unauthorized."""
        response = self.client.post('/api/auth/login/', {
            'username': 'recruiter',
            'password': 'wrongpassword',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

