from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book

BOOKS_URL = reverse("books:book-list")


class BooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", "password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            "admin@example.com", "password123"
        )
        self.book = Book.objects.create(
            title="Clean Code",
            author="Robert C. Martin",
            cover="HARD",
            inventory=5,
            daily_fee=2.50,
        )

    def test_list_books_unauthenticated(self):
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_book_as_regular_user_forbidden(self):
        self.client.force_authenticate(self.user)
        payload = {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "cover": "SOFT",
            "inventory": 3,
            "daily_fee": 1.50,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_as_admin_success(self):
        self.client.force_authenticate(self.admin)
        payload = {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "cover": "SOFT",
            "inventory": 3,
            "daily_fee": 1.50,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
