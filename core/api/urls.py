from django.urls import path  # URL routing utilities
from core.api.views import BaseInfoView  # Import aggregated stats view

urlpatterns = [
    path("base-info/", BaseInfoView.as_view(), name="base-info"),  # GET /api/base-info/
]