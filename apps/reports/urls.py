from django.urls import path
from .views import ExpenseSummaryView, ExpenseByCategoryView, ExpenseTrendView

urlpatterns = [
    path('summary/', ExpenseSummaryView.as_view(), name='expense-summary'),
    path('by-category/', ExpenseByCategoryView.as_view(), name='expense-by-category'),
    path('trend/', ExpenseTrendView.as_view(), name='expense-trend'),
]
