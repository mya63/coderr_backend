# offers_app/api/filters.py
from django_filters import rest_framework as df
from django.db.models import Min
from rest_framework.exceptions import ValidationError  # MYA

from offers_app.models import Offer


class OfferFilter(df.FilterSet):
    creator_id = df.NumberFilter(field_name="user_id")

    # filter based on annotated fields
    min_price = df.NumberFilter(method="filter_min_price")
    max_delivery_time = df.NumberFilter(method="filter_max_delivery_time")

    def filter_min_price(self, queryset, name, value):
        if value is None:
            return queryset
        # return offers where minimum price is >= given value
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        if value is None:
            return queryset
        # return offers where delivery time is <= given value
        return queryset.filter(min_delivery_time__lte=value)

    class Meta:
        model = Offer
        fields = ["creator_id", "min_price", "max_delivery_time"]