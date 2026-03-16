from django.contrib.auth.models import User
from django.db.models import Q

from offers_app.models import OfferDetail
from orders_app.models import Order


def get_user_orders(user):
    """ Return orders where the user is customer or business user."""
    return Order.objects.filter(
        Q(customer_user=user) | Q(business_user=user)
    ).distinct()


def business_user_exists(business_user_id):
    """ Check whether the business user exists."""
    return User.objects.filter(id=business_user_id).exists()


def get_in_progress_order_count(business_user_id):
    """ Count in-progress orders for a business user."""
    return Order.objects.filter(
        business_user_id=business_user_id,
        status=Order.STATUS_IN_PROGRESS,
    ).count()


def get_completed_order_count(business_user_id):
    """ Count completed orders for a business user."""
    return Order.objects.filter(
        business_user_id=business_user_id,
        status=Order.STATUS_COMPLETED,
    ).count()


def create_order_from_offer_detail(offer_detail_id, customer_user):
    """ Create an order from the selected offer detail."""
    offer_detail = OfferDetail.objects.select_related(
        "offer",
        "offer__user",
    ).get(id=offer_detail_id)

    offer = offer_detail.offer
    business_user = offer.user
    title = offer_detail.title or ""

    raw_revisions = getattr(offer_detail, "revisions", 0)
    try:
        revisions = int(raw_revisions) if raw_revisions is not None else 0
    except (TypeError, ValueError):
        revisions = 0
    if revisions < 0:
        revisions = 0

    raw_delivery = getattr(offer_detail, "delivery_time_in_days", 0)
    try:
        delivery_time_in_days = (
            int(raw_delivery) if raw_delivery is not None else 0
        )
    except (TypeError, ValueError):
        delivery_time_in_days = 0
    if delivery_time_in_days < 0:
        delivery_time_in_days = 0

    raw_price = getattr(offer_detail, "price", 0)
    price = 0 if raw_price is None else raw_price

    features = getattr(offer_detail, "features", []) or []
    offer_type = getattr(offer_detail, "offer_type", "basic") or "basic"

    return Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        title=title,
        revisions=revisions,
        delivery_time_in_days=delivery_time_in_days,
        price=price,
        features=features,
        offer_type=offer_type,
        status=Order.STATUS_IN_PROGRESS,
    )