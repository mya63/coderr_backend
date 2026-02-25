import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def business_user(db):
    user = User.objects.create_user(username="business_test", password="testpass123")
    Profile.objects.create(user=user, role=Profile.ROLE_BUSINESS)
    return user


@pytest.fixture
def customer_user(db):
    user = User.objects.create_user(username="customer_test", password="testpass123")
    Profile.objects.create(user=user, role=Profile.ROLE_CUSTOMER)
    return user


@pytest.fixture
def offer_detail(db, business_user):
    offer = Offer.objects.create(
        user=business_user,
        title="Logo Design",
        description="desc",
    )
    detail = OfferDetail.objects.create(
        offer=offer,
        offer_type="basic",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design", "Visitenkarten"],
    )
    return detail


@pytest.mark.django_db
def test_get_orders_requires_auth(api_client):
    res = api_client.get("/api/orders/")
    assert res.status_code in (401, 403)


@pytest.mark.django_db
def test_customer_can_create_order(api_client, customer_user, offer_detail):
    api_client.force_authenticate(user=customer_user)

    res = api_client.post("/api/orders/", {"offer_detail_id": offer_detail.id}, format="json")
    assert res.status_code == 201
    assert res.data["customer_user"] == customer_user.id
    assert res.data["business_user"] == offer_detail.offer.user.id
    assert res.data["status"] == "in_progress"
    assert res.data["title"] == offer_detail.offer.title


@pytest.mark.django_db
def test_business_cannot_create_order(api_client, business_user, offer_detail):
    api_client.force_authenticate(user=business_user)

    res = api_client.post("/api/orders/", {"offer_detail_id": offer_detail.id}, format="json")
    assert res.status_code == 403


@pytest.mark.django_db
def test_orders_list_returns_only_related(api_client, customer_user, business_user, offer_detail):
    # Create one related order (customer_user <-> business_user)
    order1 = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design"],
        offer_type="basic",
    )

    # Create unrelated order
    other_customer = User.objects.create_user(username="other_cust", password="x")
    Profile.objects.create(user=other_customer, role=Profile.ROLE_CUSTOMER)
    other_business = User.objects.create_user(username="other_biz", password="x")
    Profile.objects.create(user=other_business, role=Profile.ROLE_BUSINESS)

    other_offer = Offer.objects.create(user=other_business, title="X", description="Y")
    other_detail = OfferDetail.objects.create(
        offer=other_offer,
        offer_type="basic",
        revisions=1,
        delivery_time_in_days=1,
        price=10,
        features=["a"],
    )

    Order.objects.create(
        customer_user=other_customer,
        business_user=other_business,
        offer_detail=other_detail,
        title="X",
        revisions=1,
        delivery_time_in_days=1,
        price=10,
        features=["a"],
        offer_type="basic",
    )

    api_client.force_authenticate(user=customer_user)
    res = api_client.get("/api/orders/")
    assert res.status_code == 200
    ids = [o["id"] for o in res.data]
    assert order1.id in ids
    assert len(ids) == 1


@pytest.mark.django_db
def test_business_can_patch_status_only_own_order(api_client, customer_user, business_user, offer_detail):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design"],
        offer_type="basic",
        status=Order.STATUS_IN_PROGRESS,
    )

    api_client.force_authenticate(user=business_user)
    res = api_client.patch(f"/api/orders/{order.id}/", {"status": "completed"}, format="json")
    assert res.status_code == 200
    assert res.data["status"] == "completed"


@pytest.mark.django_db
def test_customer_cannot_patch_order(api_client, customer_user, business_user, offer_detail):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design"],
        offer_type="basic",
    )

    api_client.force_authenticate(user=customer_user)
    res = api_client.patch(f"/api/orders/{order.id}/", {"status": "completed"}, format="json")
    assert res.status_code == 403


@pytest.mark.django_db
def test_delete_order_admin_only(api_client, customer_user, business_user, offer_detail):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design"],
        offer_type="basic",
    )

    # Non-staff cannot delete
    api_client.force_authenticate(user=business_user)
    res = api_client.delete(f"/api/orders/{order.id}/")
    assert res.status_code == 403

    # Staff can delete
    admin = User.objects.create_user(username="admin", password="x", is_staff=True)
    api_client.force_authenticate(user=admin)
    res = api_client.delete(f"/api/orders/{order.id}/")
    assert res.status_code == 204


@pytest.mark.django_db
def test_order_count_endpoints(api_client, customer_user, business_user, offer_detail):
    # 2 in_progress, 1 completed
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design"],
        offer_type="basic",
        status=Order.STATUS_IN_PROGRESS,
    )
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design"],
        offer_type="basic",
        status=Order.STATUS_IN_PROGRESS,
    )
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design"],
        offer_type="basic",
        status=Order.STATUS_COMPLETED,
    )

    api_client.force_authenticate(user=customer_user)

    res = api_client.get(f"/api/order-count/{business_user.id}/")
    assert res.status_code == 200
    assert res.data["order_count"] == 2

    res = api_client.get(f"/api/completed-order-count/{business_user.id}/")
    assert res.status_code == 200
    assert res.data["completed_order_count"] == 1