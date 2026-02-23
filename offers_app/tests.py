import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def business_user(db):
    user = User.objects.create_user(
        username="business_test",
        password="testpass123"
    )
    Profile.objects.create(
        user=user,
        role=Profile.ROLE_BUSINESS
    )
    return user


@pytest.fixture
def customer_user(db):
    user = User.objects.create_user(
        username="customer_test",
        password="testpass123"
    )
    Profile.objects.create(
        user=user,
        role=Profile.ROLE_CUSTOMER
    )
    return user

@pytest.mark.django_db
def test_get_offers(api_client, business_user):
    api_client.force_authenticate(user=business_user)
    response = api_client.get("/api/offers/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_business_can_create_offer(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    data = {
        "title": "Test Offer",
        "description": "Beschreibung",
        "details": [
            {
                "title": "Basic",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100,
                "features": ["Logo"],
                "offer_type": "basic",
            }
        ],
    }


    response = api_client.post("/api/offers/", data, format="json")
    assert response.status_code == 201, response.data

    assert Offer.objects.count() == 1

@pytest.mark.django_db
def test_customer_cannot_create_offer(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)

    data = {
        "title": "Test Offer",
        "description": "Beschreibung",
        "details": []
    }

    response = api_client.post("/api/offers/", data, format="json")

    assert response.status_code == 403

@pytest.mark.django_db
def test_other_user_cannot_edit_offer(api_client, business_user):
    # Owner
    api_client.force_authenticate(user=business_user)
    offer = Offer.objects.create(
        user=business_user,
        title="Owner Offer",
        description="Test"
    )

    # anderer User
    other_user = User.objects.create_user(
        username="other",
        password="testpass123"
    )
    Profile.objects.create(
        user=other_user,
        role=Profile.ROLE_BUSINESS
    )

    api_client.force_authenticate(user=other_user)

    response = api_client.patch(
        f"/api/offers/{offer.id}/",
        {"title": "Hacked"},
        format="json"
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_other_user_cannot_delete_offer(api_client, business_user):
    # Owner erstellt Offer
    api_client.force_authenticate(user=business_user)
    offer = Offer.objects.create(
        user=business_user,
        title="Owner Offer",
        description="Test"
    )

    # anderer Business User
    other_user = User.objects.create_user(
        username="other",
        password="testpass123"
    )
    Profile.objects.create(
        user=other_user,
        role=Profile.ROLE_BUSINESS
    )

    api_client.force_authenticate(user=other_user)

    response = api_client.delete(f"/api/offers/{offer.id}/")
    assert response.status_code == 403

@pytest.mark.django_db
def test_owner_can_edit_offer(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    offer = Offer.objects.create(
        user=business_user,
        title="Old Title",
        description="Test"
    )

    response = api_client.patch(
        f"/api/offers/{offer.id}/",
        {"title": "New Title"},
        format="json"
    )

    assert response.status_code == 200, response.data
    offer.refresh_from_db()
    assert offer.title == "New Title"    

@pytest.mark.django_db
def test_owner_can_delete_offer(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    offer = Offer.objects.create(
        user=business_user,
        title="Delete Me",
        description="Test"
    )

    response = api_client.delete(f"/api/offers/{offer.id}/")
    assert response.status_code == 204
    assert Offer.objects.filter(id=offer.id).count() == 0


@pytest.mark.django_db
def test_get_single_offer(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    offer = Offer.objects.create(
        user=business_user,
        title="Single Offer",
        description="Test"
    )

    response = api_client.get(f"/api/offers/{offer.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Single Offer"

@pytest.mark.django_db
def test_get_offerdetail_single(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    offer = Offer.objects.create(
        user=business_user,
        title="Offer",
        description="Test"
    )

    detail = OfferDetail.objects.create(
        offer=offer,
        title="Basic",
        revisions=1,
        delivery_time_in_days=3,
        price=50,
        features=["Logo"],
        offer_type="basic"
    )

    response = api_client.get(f"/api/offerdetails/{detail.id}/")
    assert response.status_code == 200
    assert response.data["offer_type"] == "basic"