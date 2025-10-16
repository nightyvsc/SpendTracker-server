from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from apps.finances.models import Expense, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class ExpenseTrendViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="laura", password="12345")
        self.client.force_authenticate(user=self.user)
        category = Category.objects.create(name="General", user=self.user)

        today = timezone.now().date()
        Expense.objects.create(user=self.user, category=category, amount=20, date=today)
        Expense.objects.create(user=self.user, category=category, amount=30, date=today - timedelta(days=1))
        Expense.objects.create(user=self.user, category=category, amount=50, date=today - timedelta(days=2))

        self.url = reverse("expense-trend")

    def test_trend_by_day(self):
        response = self.client.get(f"{self.url}?granularity=day")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("series", data)
        self.assertGreaterEqual(len(data["series"]), 1)
