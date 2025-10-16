from django.test import SimpleTestCase
from datetime import date, timedelta
from decimal import Decimal

class ExpenseLogicUnitTest(SimpleTestCase):
    """Pruebas unitarias para verificar la lógica de agregación y porcentajes."""

    def setUp(self):
        # Datos simulados de gastos
        self.expenses = [
            {"category": "Comida", "amount": Decimal("100.00"), "date": date(2025, 10, 10)},
            {"category": "Comida", "amount": Decimal("50.00"), "date": date(2025, 10, 11)},
            {"category": "Transporte", "amount": Decimal("30.00"), "date": date(2025, 10, 10)},
            {"category": None, "amount": Decimal("20.00"), "date": date(2025, 10, 9)},
        ]

    def test_total_spending_calculation(self):
        """Verifica que el total de gastos se calcule correctamente."""
        total = sum(e["amount"] for e in self.expenses)
        self.assertEqual(total, Decimal("200.00"))

    def test_aggregate_by_category(self):
        """Prueba la agrupación manual por categoría."""
        category_totals = {}
        for e in self.expenses:
            name = e["category"] or "Uncategorized"
            category_totals[name] = category_totals.get(name, Decimal("0")) + e["amount"]

        self.assertEqual(category_totals["Comida"], Decimal("150.00"))
        self.assertEqual(category_totals["Transporte"], Decimal("30.00"))
        self.assertEqual(category_totals["Uncategorized"], Decimal("20.00"))

    def test_percentage_distribution(self):
        """Calcula porcentajes de cada categoría sobre el total."""
        total = sum(e["amount"] for e in self.expenses)
        category_totals = {"Comida": Decimal("150.00"), "Transporte": Decimal("30.00"), "Uncategorized": Decimal("20.00")}

        percentages = {k: round(v / total * 100, 2) for k, v in category_totals.items()}

        self.assertEqual(percentages["Comida"], 75.00)
        self.assertEqual(percentages["Transporte"], 15.00)
        self.assertEqual(percentages["Uncategorized"], 10.00)

    def test_trend_grouping_by_day(self):
        """Simula agrupación de gastos por día (como haría TruncDay)."""
        grouped = {}
        for e in self.expenses:
            day = e["date"]
            grouped[day] = grouped.get(day, Decimal("0")) + e["amount"]

        self.assertIn(date(2025, 10, 10), grouped)
        self.assertEqual(grouped[date(2025, 10, 10)], Decimal("130.00"))

    def test_trend_grouping_by_month(self):
        """Simula agrupación mensual (como TruncMonth)."""
        grouped = {}
        for e in self.expenses:
            month = e["date"].strftime("%Y-%m")
            grouped[month] = grouped.get(month, Decimal("0")) + e["amount"]

        self.assertEqual(grouped["2025-10"], Decimal("200.00"))
