import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from profiles_app.models import Profile
from reviews_app.models import Review


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def business_user(db):
    u = User.objects.create_user(username="biz", password="pass12345")
    Profile.objects.create(user=u, role=Profile.ROLE_BUSINESS)
    return u


@pytest.fixture
def customer_user(db):
    u = User.objects.create_user(username="cust", password="pass12345")
    Profile.objects.create(user=u, role=Profile.ROLE_CUSTOMER)
    return u


@pytest.fixture
def other_customer(db):
    u = User.objects.create_user(username="cust2", password="pass12345")
    Profile.objects.create(user=u, role=Profile.ROLE_CUSTOMER)
    return u


@pytest.mark.django_db
def test_get_reviews_requires_auth(api_client):
    res = api_client.get("/api/reviews/")
    assert res.status_code == 401


@pytest.mark.django_db
def test_get_reviews_ok_for_authenticated(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)
    res = api_client.get("/api/reviews/")
    assert res.status_code == 200


@pytest.mark.django_db
def test_customer_can_create_review(api_client, customer_user, business_user):
    api_client.force_authenticate(user=customer_user)

    res = api_client.post(
        "/api/reviews/",
        {"business_user": business_user.id, "rating": 5, "description": "Alles war toll!"},
        format="json",
    )

    assert res.status_code == 201
    data = res.json()
    assert data["business_user"] == business_user.id
    assert data["reviewer"] == customer_user.id
    assert data["rating"] == 5
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_business_cannot_create_review(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    res = api_client.post(
        "/api/reviews/",
        {"business_user": business_user.id, "rating": 5, "description": "Nope"},
        format="json",
    )

    assert res.status_code == 403


@pytest.mark.django_db
def test_only_one_review_per_business_user(api_client, customer_user, business_user):
    Review.objects.create(business_user=business_user, reviewer=customer_user, rating=4, description="ok")

    api_client.force_authenticate(user=customer_user)
    res = api_client.post(
        "/api/reviews/",
        {"business_user": business_user.id, "rating": 5, "description": "zweites mal"},
        format="json",
    )

    # UniqueConstraint -> DRF liefert i.d.R. 400
    assert res.status_code in (400, 409)
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_filter_by_business_user_id(api_client, customer_user, business_user, other_customer):
    Review.objects.create(business_user=business_user, reviewer=customer_user, rating=5, description="a")
    Review.objects.create(business_user=business_user, reviewer=other_customer, rating=3, description="b")

    api_client.force_authenticate(user=customer_user)
    res = api_client.get(f"/api/reviews/?business_user_id={business_user.id}")
    assert res.status_code == 200
    assert len(res.json()) == 2


@pytest.mark.django_db
def test_filter_by_reviewer_id(api_client, customer_user, business_user, other_customer):
    Review.objects.create(business_user=business_user, reviewer=customer_user, rating=5, description="a")
    Review.objects.create(business_user=business_user, reviewer=other_customer, rating=3, description="b")

    api_client.force_authenticate(user=customer_user)
    res = api_client.get(f"/api/reviews/?reviewer_id={customer_user.id}")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["reviewer"] == customer_user.id


@pytest.mark.django_db
def test_ordering_by_rating(api_client, customer_user, business_user, other_customer):
    Review.objects.create(business_user=business_user, reviewer=customer_user, rating=2, description="x")
    Review.objects.create(business_user=business_user, reviewer=other_customer, rating=5, description="y")

    api_client.force_authenticate(user=customer_user)
    res = api_client.get("/api/reviews/?ordering=rating")
    assert res.status_code == 200
    data = res.json()
    assert data[0]["rating"] >= data[1]["rating"]


@pytest.mark.django_db
def test_only_creator_can_patch(api_client, customer_user, other_customer, business_user):
    review = Review.objects.create(business_user=business_user, reviewer=customer_user, rating=4, description="ok")

    api_client.force_authenticate(user=other_customer)
    res = api_client.patch(f"/api/reviews/{review.id}/", {"rating": 5}, format="json")
    assert res.status_code == 403


@pytest.mark.django_db
def test_creator_can_patch(api_client, customer_user, business_user):
    review = Review.objects.create(business_user=business_user, reviewer=customer_user, rating=4, description="ok")

    api_client.force_authenticate(user=customer_user)
    res = api_client.patch(
        f"/api/reviews/{review.id}/",
        {"rating": 5, "description": "Noch besser als erwartet!"},
        format="json",
    )
    assert res.status_code == 200
    review.refresh_from_db()
    assert review.rating == 5


@pytest.mark.django_db
def test_creator_can_delete(api_client, customer_user, business_user):
    review = Review.objects.create(business_user=business_user, reviewer=customer_user, rating=4, description="ok")

    api_client.force_authenticate(user=customer_user)
    res = api_client.delete(f"/api/reviews/{review.id}/")
    assert res.status_code == 204
    assert Review.objects.count() == 0