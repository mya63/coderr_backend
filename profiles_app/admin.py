from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "first_name", "last_name")
    list_filter = ("role",)
    search_fields = ("user__username", "first_name", "last_name")