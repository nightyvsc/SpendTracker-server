from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDeleteView,
    ExpenseListCreateView, ExpenseDetailView,
    SavingsGoalListCreateView, SavingsGoalDetailView,
    DashboardSummaryView
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # Expenses
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),

    # Savings Goals
    path('savings/', SavingsGoalListCreateView.as_view(), name='savings-list-create'),
    path('savings/<int:pk>/', SavingsGoalDetailView.as_view(), name='savings-detail'),

    # Dashboard Summary
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]