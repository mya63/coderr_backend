# offers_app/api/filters.py
from django_filters import rest_framework as df
from django.db.models import Min
from rest_framework.exceptions import ValidationError  # MYA

from offers_app.models import Offer


class OfferFilter(df.FilterSet):
    creator_id = df.NumberFilter(field_name="user_id")  # MYA

    # MYA: Filter auf annotierte Werte
    min_price = df.NumberFilter(method="filter_min_price")
    max_delivery_time = df.NumberFilter(method="filter_max_delivery_time")

    def filter_min_price(self, queryset, name, value):
        if value is None:
            return queryset
        return queryset.filter(min_price__lte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        if value is None:
            return queryset
        return queryset.filter(min_delivery_time__lte=value)

    class Meta:
        model = Offer
        fields = ["creator_id", "min_price", "max_delivery_time"]