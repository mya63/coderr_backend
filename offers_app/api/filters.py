from django_filters import rest_framework as df

from offers_app.models import Offer


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