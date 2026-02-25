# offers_app/tests.py

import pytest
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


# =========================
# Deine bisherigen Tests
# =========================

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
            },
            {
                "title": "Standard",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200,
                "features": ["Logo", "Visitenkarte"],
                "offer_type": "standard",
            },
            {
                "title": "Premium",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500,
                "features": ["Logo", "Visitenkarte", "Flyer"],
                "offer_type": "premium",
            },
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
        username="other2",
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


# =========================
# MYA: Doku-Checks für GET /api/offers/
# =========================

# MYA: zusätzlicher Business-User für creator_id Filter
@pytest.fixture
def other_business_user(db):
    user = User.objects.create_user(username="business_other", password="testpass123")
    Profile.objects.create(user=user, role=Profile.ROLE_BUSINESS)
    return user


# MYA: Helper um Offer + Details zu erstellen (für min_price / min_delivery_time)
def _create_offer_with_details(owner, title="Website Design", desc="Test", prices=(100, 200), days=(7, 3)):
    offer = Offer.objects.create(user=owner, title=title, description=desc)

    OfferDetail.objects.create(
        offer=offer,
        title="Basic",
        revisions=1,
        delivery_time_in_days=days[0],
        price=prices[0],
        features=["Logo"],
        offer_type="basic",
    )
    OfferDetail.objects.create(
        offer=offer,
        title="Pro",
        revisions=2,
        delivery_time_in_days=days[1],
        price=prices[1],
        features=["Logo", "Branding"],
        offer_type="standard",
    )
    return offer


@pytest.mark.django_db
def test_get_offers_no_auth_returns_200(api_client, business_user):
    """
    MYA: Doku sagt: 'No Permissions required' -> GET /api/offers/ muss auch ohne Auth 200 liefern.
    """
    _create_offer_with_details(business_user)
    response = api_client.get("/api/offers/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_offers_is_paginated(api_client, business_user):
    """
    MYA: Doku sagt PageNumberPagination -> Response muss count/next/previous/results enthalten.
    """
    _create_offer_with_details(business_user)
    response = api_client.get("/api/offers/")
    assert response.status_code == 200

    assert "count" in response.data
    assert "next" in response.data
    assert "previous" in response.data
    assert "results" in response.data
    assert isinstance(response.data["results"], list)


@pytest.mark.django_db
def test_get_offers_result_has_required_fields(api_client, business_user):
    """
    MYA: Prüft die Doku-Felder in results[*].
    Erwartet u.a.: id,user,title,image,description,created_at,updated_at,details,min_price,min_delivery_time,user_details
    """
    _create_offer_with_details(business_user, title="Website Design", desc="Professionelles Website-Design")
    response = api_client.get("/api/offers/")
    assert response.status_code == 200

    first = response.data["results"][0]

    for key in [
        "id", "user", "title", "image", "description", "created_at", "updated_at",
        "details", "min_price", "min_delivery_time", "user_details"
    ]:
        assert key in first, f"Missing key: {key}"

    assert isinstance(first["details"], list)
    if len(first["details"]) > 0:
        assert "id" in first["details"][0]
        assert "url" in first["details"][0]

    assert isinstance(first["user_details"], dict)
    for key in ["first_name", "last_name", "username"]:
        assert key in first["user_details"]


@pytest.mark.django_db
def test_get_offers_filter_creator_id(api_client, business_user, other_business_user):
    """
    MYA: Query Param creator_id -> nur Offers von diesem Creator zurückgeben.
    """
    offer_a = _create_offer_with_details(business_user, title="A")
    _create_offer_with_details(other_business_user, title="B")

    response = api_client.get(f"/api/offers/?creator_id={business_user.id}")
    assert response.status_code == 200

    for item in response.data["results"]:
        assert item["user"] == business_user.id

    ids = [item["id"] for item in response.data["results"]]
    assert offer_a.id in ids


@pytest.mark.django_db
def test_get_offers_search(api_client, business_user):
    """
    MYA: Query Param search durchsucht title + description.
    """
    _create_offer_with_details(business_user, title="Logo Design", desc="Erstelle ein Logo")
    _create_offer_with_details(business_user, title="Website Design", desc="Professionelles Website-Design")

    response = api_client.get("/api/offers/?search=Website")
    assert response.status_code == 200

    for item in response.data["results"]:
        text = (item["title"] + " " + item["description"]).lower()
        assert "website" in text


@pytest.mark.django_db
def test_get_offers_ordering_min_price(api_client, business_user):
    """
    MYA: Query Param ordering -> z.B. min_price (aufsteigend)
    """
    _create_offer_with_details(business_user, title="Cheap", prices=(50, 70))
    _create_offer_with_details(business_user, title="Expensive", prices=(200, 300))

    response = api_client.get("/api/offers/?ordering=min_price")
    assert response.status_code == 200

    prices = [item["min_price"] for item in response.data["results"]]
    assert prices == sorted(prices)


@pytest.mark.django_db
def test_get_offers_page_size(api_client, business_user):
    """
    MYA: Query Param page_size -> begrenzt Anzahl der Ergebnisse pro Seite.
    """
    for i in range(5):
        _create_offer_with_details(business_user, title=f"Offer {i}")

    response = api_client.get("/api/offers/?page_size=2")
    assert response.status_code == 200
    assert len(response.data["results"]) <= 2

@pytest.mark.django_db
def test_offer_detail_requires_auth(api_client, business_user):
    offer = Offer.objects.create(user=business_user, title="Offer", description="Test")
    response = api_client.get(f"/api/offers/{offer.id}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_offer_detail_returns_doku_fields(api_client, business_user, other_business_user):
    # Owner erstellt Offer + 3 Details (Doku)
    offer = Offer.objects.create(user=business_user, title="Offer", description="Test")

    OfferDetail.objects.create(
        offer=offer, title="Basic", revisions=1, delivery_time_in_days=5,
        price=100, features=["Logo"], offer_type="basic"
    )
    OfferDetail.objects.create(
        offer=offer, title="Standard", revisions=2, delivery_time_in_days=7,
        price=200, features=["Logo"], offer_type="standard"
    )
    OfferDetail.objects.create(
        offer=offer, title="Premium", revisions=3, delivery_time_in_days=10,
        price=500, features=["Logo"], offer_type="premium"
    )

    # anderer eingeloggter User darf GET laut Doku
    api_client.force_authenticate(user=other_business_user)
    response = api_client.get(f"/api/offers/{offer.id}/")
    assert response.status_code == 200

    # exakt Doku keys (kein user_details!)
    expected_keys = {
        "id", "user", "title", "image", "description", "created_at", "updated_at",
        "details", "min_price", "min_delivery_time"
    }
    assert set(response.data.keys()) == expected_keys

    assert isinstance(response.data["details"], list)
    assert len(response.data["details"]) == 3
    assert "id" in response.data["details"][0]
    assert "url" in response.data["details"][0]    