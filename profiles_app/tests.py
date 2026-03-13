import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    data = {
        "username": "newuser123",
        "password": "StrongPass123",
        "type": "customer",
    }
    response = client.post("/api/registration/", data, format="json")

    assert response.status_code == 201, response.data
    assert User.objects.filter(username="newuser123").exists()