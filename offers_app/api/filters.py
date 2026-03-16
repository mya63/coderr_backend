from django.db.models import Min
from django_filters import rest_framework as df

from offers_app.models import Offer


def get_annotated_offers():
    """ Return offers with annotated min price and min delivery time."""
    return Offer.objects.all().annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min("details__delivery_time_in_days"),
    )


def get_ordered_annotated_offers():
    """ Return annotated offers ordered by latest update."""
    return get_annotated_offers().order_by("-updated_at")


class OfferFilter(df.FilterSet):
    """
    Filter offers by creator, minimum price, and maximum delivery time.
    """

    creator_id = df.NumberFilter(field_name="user_id")
    min_price = df.NumberFilter(method="filter_min_price")
    max_delivery_time = df.NumberFilter(method="filter_max_delivery_time")

    def filter_min_price(self, queryset, name, value):
        """
        Return offers whose minimum price is greater than
        or equal to the given value.
        """
        if value is None:
            return queryset
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Return offers whose minimum delivery time is less than
        or equal to the given value.
        """
        if value is None:
            return queryset
        return queryset.filter(min_delivery_time__lte=value)

    class Meta:
        model = Offer
        fields = ["creator_id", "min_price", "max_delivery_time"]