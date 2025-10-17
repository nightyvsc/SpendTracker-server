import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from accounts.models import UserProfile


@pytest.mark.django_db
class TestAccountsAPI:
    def setup_method(self):
        self.client = APIClient()

    # ---------- REGISTER ----------
    def test_register_user_creates_user_and_profile(self):
        url = reverse('signup')
        data = {
            "username": "juan",
            "email": "juan@example.com",
            "password": "12345678",
            "passwordValidator": "12345678",
            "first_name": "Juan",
            "last_name": "Díaz",
            "currency": "USD",
            "income_period": "monthly",
            "income_amount": "1000.00"
        }

        response = self.client.post(url, data, format='json')
        assert response.status_code == 201

        user = User.objects.get(username="juan")
        profile = UserProfile.objects.get(user=user)

        assert profile.currency == "USD"
        assert user.email == "juan@example.com"

    # ---------- LOGIN ----------
    def test_login_returns_tokens(self):
        user = User.objects.create_user(username='pepe', password='12345678')
        url = reverse('login')
        response = self.client.post(url, {"username": "pepe", "password": "12345678"}, format='json')

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    # ---------- PROFILE ----------
    def test_profile_retrieve_authenticated_user(self):
        user = User.objects.create_user(username='ana', password='testpass')
        UserProfile.objects.create(user=user, currency="USD")

        # Login to get token
        login_url = reverse('login')
        token_resp = self.client.post(login_url, {"username": "ana", "password": "testpass"}, format='json')
        token = token_resp.data["access"]

        # Use token for authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        profile_url = reverse('profile')
        resp = self.client.get(profile_url)

        assert resp.status_code == 200
        assert resp.data["username"] == "ana"

    # ---------- CHANGE PASSWORD ----------
    def test_change_password_with_correct_old_password(self):
        user = User.objects.create_user(username='carlos', password='oldpass')
        UserProfile.objects.create(user=user)

        login_resp = self.client.post(reverse('login'), {"username": "carlos", "password": "oldpass"}, format='json')
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {
            "old_password": "oldpass",
            "new_password": "newpass",
            "new_passwordValidator": "newpass"
        }
        resp = self.client.put(reverse('change-password'), data, format='json')
        assert resp.status_code == 200

        # Verify new password works
        login_check = self.client.post(reverse('login'), {"username": "carlos", "password": "newpass"}, format='json')
        assert login_check.status_code == 200
