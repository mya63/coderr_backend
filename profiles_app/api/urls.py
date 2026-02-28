from django.urls import path
from .views import (
    ProfileDetailView,
    BusinessProfilesListView,
    CustomerProfilesListView,
)

urlpatterns = [
    # Doku-konform (wie du es bereits hattest)
    path("profiles/business/", BusinessProfilesListView.as_view(), name="business-profiles"),
    path("profiles/customer/", CustomerProfilesListView.as_view(), name="customer-profiles"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profiles-detail"),

    # 🔥 Frontend erwartet singular:
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail-frontend"),
]