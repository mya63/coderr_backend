from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from profiles_app.models import Profile
from reviews_app.models import Review


class BaseInfoView(APIView):
    """
    Return basic platform statistics for the public API.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Return review count, average rating, business profile count,
        and offer count.
        """
        review_count = Review.objects.count()
        avg = Review.objects.aggregate(avg=Avg("rating"))["avg"]
        average_rating = round(float(avg), 1) if avg is not None else 0.0

        business_profile_count = Profile.objects.filter(
            role=Profile.ROLE_BUSINESS
        ).count()

        offer_count = Offer.objects.count()

        return Response(
            {
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
        )