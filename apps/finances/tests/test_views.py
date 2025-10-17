from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from apps.finances.models import Category, Expense, SavingsGoal
from django.contrib.auth import get_user_model

User = get_user_model()

class FinanceViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carlos", password="12345")
        self.client.force_authenticate(user=self.user)

        # Base URLs
        self.url_categories = reverse("category-list-create")
        self.url_expenses = reverse("expense-list-create")
        self.url_savings = reverse("savings-list-create")
        self.url_dashboard = reverse("dashboard-summary")

    # --- CATEGORY TESTS ---

    def test_create_category(self):
        response = self.client.post(self.url_categories, {"name": "Food", "icon": "icon-food", "color": "#FF0000"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().user, self.user)

    def test_list_only_user_categories(self):
        Category.objects.create(name="Food", user=self.user)
        other_user = User.objects.create_user(username="notme", password="123")
        Category.objects.create(name="OtherCat", user=other_user)

        response = self.client.get(self.url_categories)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], "Food")

    def test_delete_category(self):
        category = Category.objects.create(name="Temp", user=self.user)
        url_delete = reverse("category-delete", args=[category.id])

        response = self.client.delete(url_delete)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 0)

    # --- EXPENSE TESTS ---

    def test_create_expense(self):
        category = Category.objects.create(name="Food", user=self.user)
        today = timezone.now().date()

        response = self.client.post(self.url_expenses, {
            "category": category.id,
            "amount": "50.00",
            "date": today
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().user, self.user)

    def test_list_only_user_expenses(self):
        category = Category.objects.create(name="Food", user=self.user)
        Expense.objects.create(user=self.user, category=category, amount=100, date=timezone.now().date())

        other_user = User.objects.create_user(username="xuser", password="123")
        Expense.objects.create(user=other_user, category=category, amount=999, date=timezone.now().date())

        response = self.client.get(self.url_expenses)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(float(response.json()[0]["amount"]), 100.0)

    def test_update_expense(self):
        category = Category.objects.create(name="Food", user=self.user)
        expense = Expense.objects.create(user=self.user, category=category, amount=40, date=timezone.now().date())

        url_detail = reverse("expense-detail", args=[expense.id])
        response = self.client.patch(url_detail, {"amount": "60.00"})
        self.assertEqual(response.status_code, 200)
        expense.refresh_from_db()
        self.assertEqual(float(expense.amount), 60.0)

    def test_delete_expense(self):
        category = Category.objects.create(name="Food", user=self.user)
        expense = Expense.objects.create(user=self.user, category=category, amount=20, date=timezone.now().date())

        url_detail = reverse("expense-detail", args=[expense.id])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Expense.objects.count(), 0)

    # --- SAVINGS GOALS TESTS ---

    def test_create_savings_goal(self):
        response = self.client.post(self.url_savings, {
            "name": "Emergency Fund",
            "target_amount": "1000.00",
            "current_amount": "200.00"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavingsGoal.objects.count(), 1)
        self.assertEqual(SavingsGoal.objects.first().user, self.user)

    def test_list_savings_goals(self):
        SavingsGoal.objects.create(user=self.user, name="Trip", target_amount=500, current_amount=100)
        response = self.client.get(self.url_savings)
        self.assertEqual(len(response.json()), 1)

    # --- DASHBOARD SUMMARY TEST ---

    def test_dashboard_summary(self):
        category = Category.objects.create(name="Food", user=self.user)
        Expense.objects.create(user=self.user, category=category, amount=100, date=timezone.now().date())

        SavingsGoal.objects.create(user=self.user, name="Trip", target_amount=500, current_amount=250)

        response = self.client.get(self.url_dashboard)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_spent", data)
        self.assertIn("current_balance", data)
        self.assertIn("savings_goals", data)
        self.assertEqual(float(data["total_spent"]), 100.0)
