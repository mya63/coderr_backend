from django.urls import path
from .views import (
    ProfileDetailView,
    BusinessProfilesListView,
    CustomerProfilesListView,
)

urlpatterns = [
    
    path("profiles/business/", BusinessProfilesListView.as_view(), name="business-profiles"),
    path("profiles/customer/", CustomerProfilesListView.as_view(), name="customer-profiles"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profiles-detail"),

    
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail-frontend"),
]