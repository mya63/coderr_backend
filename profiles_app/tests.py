import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    data = {"username": "newuser123", "password": "StrongPass123", "type": "customer"}
    response = client.post("/api/registration/", data, format="json")

    # Debug nur wenn Test failt (hilft dir mega beim Lernen)
    assert response.status_code == 201, response.data

    assert User.objects.filter(username="newuser123").exists()