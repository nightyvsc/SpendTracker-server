from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from apps.finances.models import Expense, Category

class ExpenseSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        daily = Expense.objects.filter(user=user).values('date').annotate(total=Sum('amount')).order_by('-date')[:7]
        monthly = Expense.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('-month')[:6]

        return Response({
            "total": total,
            "daily": list(daily),
            "monthly": list(monthly),
        })


class ExpenseByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount')).order_by('-total')
        return Response(list(data))


class ExpenseTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        trend = Expense.objects.filter(user=user).annotate(week=TruncWeek('date')).values('week').annotate(total=Sum('amount')).order_by('week')
        return Response(list(trend))

