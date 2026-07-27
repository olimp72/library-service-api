from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

USER_URL = reverse("users:create")

class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser("admin@example.com", "adminpass")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_api_success(self):
        payload = {
            "email": "user@example.com",
            "password": "password123",
        }
        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)
