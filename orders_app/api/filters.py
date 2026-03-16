from django.contrib.auth.models import User
from django.db.models import Q

from orders_app.models import Order

def get_user_orders(user):
    return Order.objects.filter(
        Q(customer_user=user) | Q(business_user=user)
    ).distinct()


def business_user_exists(business_user_id):
    return User.objects.filter(id=business_user_id).exists()


def get_in_progress_order_count(business_user_id):
    return Order.objects.filter(
        business_user_id=business_user_id,
        status=Order.STATUS_IN_PROGRESS,
    ).count()


def get_completed_order_count(business_user_id):
    return Order.objects.filter(
        business_user_id=business_user_id,
        status=Order.STATUS_COMPLETED,
    ).count()