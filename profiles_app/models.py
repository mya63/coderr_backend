from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_BUSINESS = "business"
    ROLE_CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ROLE_BUSINESS, "Business"),
        (ROLE_CUSTOMER, "Customer"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Doku: "type" -> wir speichern intern role, geben aber im Serializer "type" zurück
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")

    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")

    # Doku: "file" (als String/URL). Für den Anfang als optionales Bildfeld:
    file = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"