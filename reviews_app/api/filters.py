from reviews_app.models import Review


def get_filtered_reviews(request):
    queryset = Review.objects.all()

    business_user_id = request.query_params.get("business_user_id")
    reviewer_id = request.query_params.get("reviewer_id")
    ordering = request.query_params.get("ordering")

    if business_user_id:
        queryset = queryset.filter(business_user_id=business_user_id)

    if reviewer_id:
        queryset = queryset.filter(reviewer_id=reviewer_id)

    if ordering == "rating":
        queryset = queryset.order_by("-rating", "-updated_at")
    elif ordering == "updated_at":
        queryset = queryset.order_by("-updated_at")

    return queryset