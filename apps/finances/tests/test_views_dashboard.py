# test_views_dashboard.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.finances.models import Expense, SavingsGoal
from datetime import date

@pytest.mark.django_db
class TestDashboardSummaryView:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.url = reverse("dashboard-summary")

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        assert response.status_code == 401  # unauthorized

    def test_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        data = response.json()

        assert response.status_code == 200
        assert data["total_spent"] == 0
        assert data["current_balance"] == 0
        assert data["savings_goals"] == []

    def test_with_expenses_and_no_income(self):
        self.client.force_authenticate(user=self.user)
        Expense.objects.create(user=self.user, amount=100, date=date.today())

        response = self.client.get(self.url)
        data = response.json()

        assert data["total_spent"] == 100
        assert data["current_balance"] == -100  # because income_amount defaults to 0

    def test_savings_goal_zero_target(self):
        self.client.force_authenticate(user=self.user)
        SavingsGoal.objects.create(user=self.user, name="Test Goal", target_amount=0, current_amount=50)

        response = self.client.get(self.url)
        data = response.json()
        goal = data["savings_goals"][0]

        assert goal["progress"] == 0  # no division by zero

    def test_savings_goal_correct_progress(self):
        self.client.force_authenticate(user=self.user)
        SavingsGoal.objects.create(user=self.user, name="Progress Goal", target_amount=200, current_amount=50)

        response = self.client.get(self.url)
        data = response.json()
        goal = data["savings_goals"][0]

        assert goal["progress"] == 25  # 50/200 * 100

    def test_only_goals_no_expenses(self):
        self.client.force_authenticate(user=self.user)
        SavingsGoal.objects.create(user=self.user, name="Only Goal", target_amount=100, current_amount=40)

        response = self.client.get(self.url)
        data = response.json()

        assert data["total_spent"] == 0
        assert data["current_balance"] == 0
        assert len(data["savings_goals"]) == 1
