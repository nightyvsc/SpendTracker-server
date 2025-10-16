from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal

from apps.finances.models import Expense
from .serializers import (
    SummaryQuerySerializer,
    ByCategoryQuerySerializer,
    TrendQuerySerializer,
)

class ExpenseSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = SummaryQuerySerializer(data=request.query_params)
        q.is_valid(raise_exception=True)
        start = q.validated_data.get("start")
        end = q.validated_data.get("end")
        daily_limit = q.validated_data["daily_limit"]
        monthly_limit = q.validated_data["monthly_limit"]

        qs = Expense.objects.filter(user=request.user)
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)

        total = qs.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        # últimos N días (orden descendente por fecha)
        daily = (
            qs.values("date")
              .annotate(total=Sum("amount"))
              .order_by("-date")[:daily_limit]
        )
        daily = [{"date": r["date"], "total": float(r["total"] or 0)} for r in daily]

        # últimos N meses (por mes)
        monthly = (
            qs.annotate(month=TruncMonth("date"))
              .values("month")
              .annotate(total=Sum("amount"))
              .order_by("-month")[:monthly_limit]
        )
        monthly = [{"month": r["month"].strftime("%Y-%m"), "total": float(r["total"] or 0)} for r in monthly]

        return Response({
            "filters": {
                "start": str(start) if start else None,
                "end": str(end) if end else None,
                "daily_limit": daily_limit,
                "monthly_limit": monthly_limit,
            },
            "total": float(total),
            "daily": daily,
            "monthly": monthly,
        })


class ExpenseByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = ByCategoryQuerySerializer(data=request.query_params)
        q.is_valid(raise_exception=True)
        start = q.validated_data.get("start")
        end = q.validated_data.get("end")
        include_uncategorized = q.validated_data["include_uncategorized"]
        top_n = q.validated_data.get("top_n")

        qs = Expense.objects.filter(user=request.user)
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)

        data = (
            qs.values("category__name")
              .annotate(total=Sum("amount"))
              .order_by("-total")
        )

        # Mapear categoría nula
        mapped = []
        for r in data:
            name = r["category__name"] if r["category__name"] else "Uncategorized"
            if name == "Uncategorized" and not include_uncategorized:
                continue
            mapped.append({"category": name, "total": float(r["total"] or 0)})

        if top_n:
            mapped = mapped[:top_n]

        total_spending = sum(item["total"] for item in mapped) if mapped else 0.0
        # porcentajes útiles para UI
        for item in mapped:
            item["pct"] = round((item["total"] / total_spending * 100), 2) if total_spending else 0.0

        return Response({
            "filters": {
                "start": str(start) if start else None,
                "end": str(end) if end else None,
                "include_uncategorized": include_uncategorized,
                "top_n": top_n,
            },
            "total_spending": total_spending,
            "by_category": mapped,
        })


class ExpenseTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = TrendQuerySerializer(data=request.query_params)
        q.is_valid(raise_exception=True)
        start = q.validated_data.get("start")
        end = q.validated_data.get("end")
        gran = q.validated_data["granularity"]

        qs = Expense.objects.filter(user=request.user)
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)

        if gran == "day":
            qs = (qs.annotate(period=TruncDay("date"))
                    .values("period")
                    .annotate(total=Sum("amount"))
                    .order_by("period"))
            series = [{"period": r["period"].strftime("%Y-%m-%d"), "total": float(r["total"] or 0)} for r in qs]

        elif gran == "week":
            qs = (qs.annotate(period=TruncWeek("date"))
                    .values("period")
                    .annotate(total=Sum("amount"))
                    .order_by("period"))
            # Django retorna un date de inicio de semana; lo serializamos ISO
            series = [{"period": r["period"].strftime("%Y-%m-%d"), "total": float(r["total"] or 0)} for r in qs]

        else:  # "month"
            qs = (qs.annotate(period=TruncMonth("date"))
                    .values("period")
                    .annotate(total=Sum("amount"))
                    .order_by("period"))
            series = [{"period": r["period"].strftime("%Y-%m"), "total": float(r["total"] or 0)} for r in qs]

        return Response({
            "filters": {
                "start": str(start) if start else None,
                "end": str(end) if end else None,
                "granularity": gran,
            },
            "series": series,
        })
