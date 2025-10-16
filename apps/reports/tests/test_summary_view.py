from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from apps.finances.models import Expense, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class ExpenseSummaryViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(name="Comida", user=self.user)
        today = timezone.now().date()

        Expense.objects.create(user=self.user, category=category, amount=50, date=today)
        Expense.objects.create(user=self.user, category=category, amount=100, date=today)

        self.url = reverse("expense-summary")  

    def test_summary_total_and_daily_monthly_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("total", data)
        self.assertEqual(data["total"], 150.0)
        self.assertIn("daily", data)
        self.assertGreater(len(data["daily"]), 0)
        self.assertIn("monthly", data)
