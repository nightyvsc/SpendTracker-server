from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Category, Expense, SavingsGoal
from .serializers import CategorySerializer, ExpenseSerializer, SavingsGoalSerializer
from .utils import get_period_spendings, get_current_balance


# --- CATEGORY CRUD ---

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


# --- EXPENSE CRUD ---

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


# --- SAVINGS GOALS CRUD ---

class SavingsGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingsGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class DashboardSummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        period = 'monthly'  

        total_spent = get_period_spendings(user, period)
       
        current_balance = get_current_balance(user, income_amount=0, period=period)

        goals = SavingsGoal.objects.filter(user=user)
        goals_data = []
        for goal in goals:
            goals_data.append({
                "name": goal.name,
                "target": goal.target_amount,
                "current": goal.current_amount,
                "progress": (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
            })

        return Response({
            "period": period,
            "total_spent": total_spent,
            "current_balance": current_balance,
            "savings_goals": goals_data
        })