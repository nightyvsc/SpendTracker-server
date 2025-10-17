from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.finances.models import Category, Expense, SavingsGoal

User = get_user_model()

class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.category = Category.objects.create(
            name="Food", icon="🍔", color="#FF0000", user=self.user
        )

    def test_string_representation(self):
        self.assertEqual(str(self.category), "Food (tester)")

    def test_category_belongs_to_user(self):
        self.assertEqual(self.category.user, self.user)


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.category = Category.objects.create(name="Transport", user=self.user)
        self.expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=50,
            date=timezone.now().date(),
            description="Bus ticket"
        )

    def test_string_representation(self):
        expected = f"{self.expense.amount} - {self.user.username} - {self.expense.date}"
        self.assertEqual(str(self.expense), expected)

    def test_expense_defaults(self):
        self.assertIsNotNone(self.expense.created_at)

    def test_category_set_null_on_delete(self):
        self.category.delete()
        self.expense.refresh_from_db()
        self.assertIsNone(self.expense.category)


class SavingsGoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.goal = SavingsGoal.objects.create(
            user=self.user,
            name="Emergency Fund",
            target_amount=1000,
            current_amount=0
        )

    def test_string_representation(self):
        self.assertEqual(str(self.goal), "Emergency Fund - tester")

    def test_default_current_amount(self):
        self.assertEqual(self.goal.current_amount, 0)

    def test_goal_belongs_to_user(self):
        self.assertEqual(self.goal.user, self.user)
