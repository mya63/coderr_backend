from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """
    Store the main offer data created by a business user.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="offers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the offer title.
        """
        return self.title


class OfferDetail(models.Model):
    """
    Store a specific pricing tier and feature set for an offer.
    """

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.FloatField()
    features = models.JSONField(default=list, blank=True)

    OFFER_TYPES = (
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium"),
    )
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)

    def __str__(self):
        """
        Return a readable label for the offer detail.
        """
        return f"{self.offer.title} - {self.offer_type}"