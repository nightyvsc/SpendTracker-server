from rest_framework import serializers
from .models import Category, Expense, SavingsGoal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'color', 'user']
        read_only_fields = ['user']

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)  # Para tener info completa
    
    class Meta:
        model = Expense
        fields = [
            'id', 'date', 'category', 'category_name', 'category_details',
            'amount', 'description', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class SavingsGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = SavingsGoal
        fields = [
            'id', 'user', 'name', 'target_amount',
            'current_amount', 'deadline', 'progress_percentage'
        ]
        read_only_fields = ['user']

    def get_progress_percentage(self, obj):
        if obj.target_amount > 0:
            return float(obj.current_amount / obj.target_amount) * 100
        return 0