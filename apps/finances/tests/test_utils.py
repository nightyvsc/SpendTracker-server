from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from apps.finances.utils import (
    get_current_period_dates,
    get_period_spendings,
    get_current_balance
)
from apps.finances.models import Expense, Category

User = get_user_model()

class UtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.category = Category.objects.create(name="TestCat", user=self.user)

    # --- get_current_period_dates tests ---

    def test_daily_period_dates(self):
        start, end = get_current_period_dates("daily")
        today = date.today()
        self.assertEqual(start, today)
        self.assertEqual(end, today)

    def test_weekly_period_dates(self):
        start, end = get_current_period_dates("weekly")
        expected_start = date.today() - timedelta(days=date.today().weekday())  # Monday
        expected_end = expected_start + timedelta(days=6)  # Sunday
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_monthly_period_dates(self):
        start, end = get_current_period_dates("monthly")
        today = date.today()
        expected_start = date(today.year, today.month, 1)
        if today.month == 12:
            expected_end = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            expected_end = date(today.year, today.month + 1, 1) - timedelta(days=1)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_yearly_period_dates(self):
        start, end = get_current_period_dates("yearly")
        today = date.today()
        self.assertEqual(start, date(today.year, 1, 1))
        self.assertEqual(end, date(today.year, 12, 31))

    # --- Spendings & Balance tests ---

    def test_get_period_spendings(self):
        today = timezone.now().date()
        Expense.objects.create(user=self.user, category=self.category, amount=50, date=today)
        Expense.objects.create(user=self.user, category=self.category, amount=30, date=today)

        total_spent = get_period_spendings(self.user, period="monthly")
        self.assertEqual(float(total_spent), 80.0)

    def test_get_period_spendings_returns_zero_if_no_expenses(self):
        total_spent = get_period_spendings(self.user, period="monthly")
        self.assertEqual(float(total_spent), 0.0)

    def test_get_current_balance(self):
        today = timezone.now().date()
        # Add expenses to reduce balance
        Expense.objects.create(user=self.user, category=self.category, amount=20, date=today)
        Expense.objects.create(user=self.user, category=self.category, amount=30, date=today)

        balance = get_current_balance(self.user, income_amount=200, period="monthly")
        self.assertEqual(balance, 150.0)  # 200 - 50 = 150
