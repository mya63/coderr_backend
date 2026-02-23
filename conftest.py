# conftest.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from profiles_app.models import Profile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def business_user(db):
    # MYA: Business-User + Profile(role="business") für Permissions
    user = User.objects.create_user(username="business_test", password="test12345")
    Profile.objects.create(user=user, role=Profile.ROLE_BUSINESS)
    return user

@pytest.fixture
def customer_user(db):
    # MYA: Customer-User + Profile(role="customer")
    user = User.objects.create_user(username="customer_test", password="test12345")
    Profile.objects.create(user=user, role=Profile.ROLE_CUSTOMER)
    return user