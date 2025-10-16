from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from apps.finances.models import Expense, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class ExpenseByCategoryViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carlos", password="12345")
        self.client.force_authenticate(user=self.user)
        today = timezone.now().date()

        cat_food = Category.objects.create(name="Comida", user=self.user)
        cat_ent = Category.objects.create(name="Entretenimiento", user=self.user)

        Expense.objects.create(user=self.user, category=cat_food, amount=60, date=today)
        Expense.objects.create(user=self.user, category=cat_ent, amount=40, date=today)

        self.url = reverse("expense-by-category")

    def test_by_category_returns_correct_totals(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_spending"], 100.0)
        categories = [c["category"] for c in data["by_category"]]
        self.assertIn("Comida", categories)
        self.assertIn("Entretenimiento", categories)
