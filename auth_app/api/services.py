from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile

User = get_user_model()


# MYA START - demo users for guest login
DEMO_USERS = [
    {
        "username": "DemoBusiness",
        "email": "demo-business@example.com",
        "password": "asdasd24",
        "role": Profile.ROLE_BUSINESS,
    },
    {
        "username": "DemoCustomer",
        "email": "demo-customer@example.com",
        "password": "asdasd12",
        "role": Profile.ROLE_CUSTOMER,
    },
]


def ensure_demo_users():
    """
    Create or update fixed demo users for guest login.
    """
    for demo_user in DEMO_USERS:
        user, _ = User.objects.get_or_create(
            username=demo_user["username"],
            defaults={"email": demo_user["email"]},
        )

        user.email = demo_user["email"]
        user.set_password(demo_user["password"])
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = demo_user["role"]
        profile.save()

        Token.objects.get_or_create(user=user)

def register_user_with_profile(user, role):
    """
    Create a profile for the new user and return an auth token.
    """
    Profile.objects.create(user=user, role=role)

    token, _ = Token.objects.get_or_create(user=user)
    return token


def login_user_and_get_token(user):
    """
    Return an existing or new authentication token.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token