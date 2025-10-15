from datetime import date, timedelta
from django.db.models import Sum
from .models import Expense

def get_current_period_dates(period='monthly'):
    """
    Return (start_date, end_date) based on the user's income period.
    Available values: 'daily', 'weekly', 'monthly', 'yearly'
    """
    today = date.today()

    if period == 'daily':
        return today, today

    if period == 'weekly':
        start = today - timedelta(days=today.weekday())  # Monday
        end = start + timedelta(days=6)  # Sunday
        return start, end

    if period == 'monthly':
        start = date(today.year, today.month, 1)
        if today.month == 12:
            end = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(today.year, today.month + 1, 1) - timedelta(days=1)
        return start, end

    if period == 'yearly':
        start = date(today.year, 1, 1)
        end = date(today.year, 12, 31)
        return start, end

    return today, today  # fallback


def get_period_spendings(user, period='monthly'):
    """
    Returns total spent by the user in the given period.
    """
    start, end = get_current_period_dates(period)
    total = Expense.objects.filter(user=user, date__range=(start, end)).aggregate(Sum('amount'))['amount__sum']
    return total or 0


def get_current_balance(user, income_amount=0, period='monthly'):
    """
    Returns current balance = income - expenses in period.
    income_amount can later come from an Income model or user profile.
    """
    spendings = get_period_spendings(user, period)
    return float(income_amount) - float(spendings)