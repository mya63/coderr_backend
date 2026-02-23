from django.urls import path

from .views import (
    BusinessProfilesListView,
    CustomerProfilesListView,
    ProfileDetailView,
)

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profiles/business/", BusinessProfilesListView.as_view(), name="profiles-business"),
    path("profiles/customer/", CustomerProfilesListView.as_view(), name="profiles-customer"),
]