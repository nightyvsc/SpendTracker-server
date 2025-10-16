from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.finances.models import Category, Expense, SavingsGoal
from apps.finances.serializers import CategorySerializer, ExpenseSerializer, SavingsGoalSerializer

User = get_user_model()

class CategorySerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.category = Category.objects.create(
            name="Food", icon="🍕", color="#FF5733", user=self.user
        )

    def test_serialization(self):
        serializer = CategorySerializer(self.category)
        data = serializer.data
        self.assertEqual(data["name"], "Food")
        self.assertEqual(data["icon"], "🍕")
        self.assertEqual(data["color"], "#FF5733")
        self.assertEqual(data["user"], self.user.id)

    def test_user_is_read_only(self):
        payload = {
            "name": "New Category",
            "icon": "🎮",
            "color": "#000000",
            "user": 999  # Trying to override user
        }
        serializer = CategorySerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save(user=self.user)
        self.assertEqual(instance.user, self.user)  # Should not override with 999


class ExpenseSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.category = Category.objects.create(name="Transport", user=self.user)
        self.expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=50,
            date=timezone.now().date(),
            description="Taxi"
        )

    def test_serialization(self):
        serializer = ExpenseSerializer(self.expense)
        data = serializer.data
        self.assertEqual(data["amount"], "50.00")
        self.assertEqual(data["category"], self.category.id)
        self.assertEqual(data["category_name"], "Transport")
        self.assertEqual(data["user"], self.user.id)

    def test_user_and_created_at_are_read_only(self):
        payload = {
            "amount": 80,
            "date": timezone.now().date(),
            "description": "Override test",
            "user": 999,  # Trying to override user
            "created_at": "2020-01-01T00:00:00Z"
        }
        serializer = ExpenseSerializer(data=payload)
        self.assertTrue(serializer.is_valid())


class SavingsGoalSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.goal = SavingsGoal.objects.create(
            user=self.user,
            name="Vacation",
            target_amount=1000,
            current_amount=200
        )

    def test_serialization_with_progress(self):
        serializer = SavingsGoalSerializer(self.goal)
        data = serializer.data
        expected_progress = (200 / 1000) * 100
        self.assertEqual(data["name"], "Vacation")
        self.assertAlmostEqual(data["progress_percentage"], expected_progress, places=2)

    def test_progress_percentage_zero_if_no_target(self):
        goal = SavingsGoal.objects.create(
            user=self.user,
            name="No Target",
            target_amount=0,
            current_amount=200
        )
        serializer = SavingsGoalSerializer(goal)
        data = serializer.data
        self.assertEqual(data["progress_percentage"], 0)