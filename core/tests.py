import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from profiles_app.models import Profile
from offers_app.models import Offer
from reviews_app.models import Review


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_base_info_no_permissions_required(api_client):
    res = api_client.get("/api/base-info/")
    assert res.status_code == 200


@pytest.mark.django_db
def test_base_info_returns_correct_stats(api_client):
    # business users
    b1 = User.objects.create_user(username="biz1", password="pass12345")
    b2 = User.objects.create_user(username="biz2", password="pass12345")
    Profile.objects.create(user=b1, role=Profile.ROLE_BUSINESS)
    Profile.objects.create(user=b2, role=Profile.ROLE_BUSINESS)

    # customer
    c1 = User.objects.create_user(username="cust1", password="pass12345")
    Profile.objects.create(user=c1, role=Profile.ROLE_CUSTOMER)

    # offers
    Offer.objects.create(user=b1, title="Offer 1", description="x")
    Offer.objects.create(user=b2, title="Offer 2", description="y")

    # reviews (avg = (5+4)/2 = 4.5)
    Review.objects.create(business_user=b1, reviewer=c1, rating=5, description="a")
    c2 = User.objects.create_user(username="cust2", password="pass12345")
    Profile.objects.create(user=c2, role=Profile.ROLE_CUSTOMER)
    Review.objects.create(business_user=b2, reviewer=c2, rating=4, description="b")

    res = api_client.get("/api/base-info/")
    assert res.status_code == 200
    data = res.json()

    assert data["review_count"] == 2
    assert data["average_rating"] == 4.5
    assert data["business_profile_count"] == 2
    assert data["offer_count"] == 2