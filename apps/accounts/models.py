from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=False)
    currency = models.CharField(max_length=3, default='USD')
    income_period = models.CharFiel(max_length=20, choices = [
        'weekly', 'biweekly', 'monthly'
    ], default = 'monthly')

    income_amount = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    