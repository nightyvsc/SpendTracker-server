# test_urls.py
import pytest
from django.urls import reverse, resolve
from apps.finances.views import (
    CategoryListCreateView,
    CategoryDeleteView,
    ExpenseListCreateView,
    ExpenseDetailView,
    SavingsGoalListCreateView,
    SavingsGoalDetailView,
    DashboardSummaryView,
)

@pytest.mark.django_db
class TestURLs:

    def test_category_list_create_url(self):
        path = reverse('category-list-create')
        assert resolve(path).func.view_class == CategoryListCreateView

    def test_category_delete_url(self):
        path = reverse('category-delete', kwargs={'pk': 1})
        assert resolve(path).func.view_class == CategoryDeleteView

    def test_expense_list_create_url(self):
        path = reverse('expense-list-create')
        assert resolve(path).func.view_class == ExpenseListCreateView

    def test_expense_detail_url(self):
        path = reverse('expense-detail', kwargs={'pk': 1})
        assert resolve(path).func.view_class == ExpenseDetailView

    def test_savings_list_create_url(self):
        path = reverse('savings-list-create')
        assert resolve(path).func.view_class == SavingsGoalListCreateView

    def test_savings_detail_url(self):
        path = reverse('savings-detail', kwargs={'pk': 1})
        assert resolve(path).func.view_class == SavingsGoalDetailView

    def test_dashboard_summary_url(self):
        path = reverse('dashboard-summary')
        assert resolve(path).func.view_class == DashboardSummaryView
