from django.shortcuts import get_object_or_404

from profiles_app.models import Profile


def get_profile_by_user_id(user_id):
    """
    Return a profile by related user id.
    """
    return get_object_or_404(
        Profile.objects.select_related("user"),
        user_id=user_id,
    )


def get_business_profiles():
    """
    Return all business profiles.
    """
    return Profile.objects.select_related("user").filter(
        role=Profile.ROLE_BUSINESS
    )


def get_customer_profiles():
    """
    Return all customer profiles.
    """
    return Profile.objects.select_related("user").filter(
        role=Profile.ROLE_CUSTOMER
    )