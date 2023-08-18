import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_phone_number = "1234567890"
        self.invalid_phone_number = "12345"

    def test_valid_phone_number(self):
        response = self.client.post('http://localhost:8000/user/auth/auth/', {'phone_number': self.valid_phone_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

    def test_invalid_phone_number(self):
        response = self.client.post('http://localhost:8000/user/auth/auth/', {'phone_number': self.invalid_phone_number})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_missing_phone_number(self):
        response = self.client.post('http://localhost:8000/user/auth/auth/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_valid_code(self):
        self.client.post('http://localhost:8000/user/auth/auth/', {'phone_number': self.valid_phone_number})
        random_code = self.client.session['random_code']

        response = self.client.post('http://localhost:8000/user/auth/accept_user/', {'code': random_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data[1])

    def test_invalid_code(self):
        self.client.post('http://localhost:8000/user/auth/auth/', {'phone_number': self.valid_phone_number})

        response = self.client.post('http://localhost:8000/user/auth/accept_user/', {'code': 1234})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_missing_code(self):
        response = self.client.post('http://localhost:8000/user/auth/accept_user/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
