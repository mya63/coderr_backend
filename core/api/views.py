from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from reviews_app.models import Review
from profiles_app.models import Profile
from offers_app.models import Offer


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        review_count = Review.objects.count()

        avg = Review.objects.aggregate(avg=Avg("rating"))["avg"]
        average_rating = round(float(avg), 1) if avg is not None else 0.0

        business_profile_count = Profile.objects.filter(role=Profile.ROLE_BUSINESS).count()
        offer_count = Offer.objects.count()

        return Response(
            {
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
        )