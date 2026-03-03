from django.db.models import Avg  # Used for calculating average rating
from rest_framework.views import APIView  # Base class for custom API views
from rest_framework.response import Response  # Standard DRF response
from rest_framework.permissions import AllowAny  # No authentication required

from reviews_app.models import Review  # Review model
from profiles_app.models import Profile  # Profile model
from offers_app.models import Offer  # Offer model


class BaseInfoView(APIView):
    permission_classes = [AllowAny]  # Public endpoint (no auth required)

    def get(self, request):
        review_count = Review.objects.count()  # Total number of reviews

        avg = Review.objects.aggregate(avg=Avg("rating"))["avg"]  # Calculate average rating
        average_rating = round(float(avg), 1) if avg is not None else 0.0  # Round to 1 decimal

        business_profile_count = Profile.objects.filter(
            role=Profile.ROLE_BUSINESS
        ).count()  # Count business profiles

        offer_count = Offer.objects.count()  # Total number of offers

        return Response(
            {
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
        )