from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class AdminUser(admin.ModelAdmin):
    list_display = ['user', 'currency', 'income_period', 'income_amount']
    search_fields = ['user__username', 'full_name']