from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from borrowings.models import Borrowing

BORROWINGS_URL = reverse("borrowings:borrowing-list")

class BorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user@example.com", "password123")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=2,
            daily_fee=1.00,
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing_success(self):
        payload = {
            "expected_return_date": date.today() + timedelta(days=7),
            "book": self.book.id,
        }
        res = self.client.post(BORROWINGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 1)

    def test_create_borrowing_out_of_stock_fails(self):
        self.book.inventory = 0
        self.book.save()
        payload = {
            "expected_return_date": date.today() + timedelta(days=7),
            "book": self.book.id,
        }
        res = self.client.post(BORROWINGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
