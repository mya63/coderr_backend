from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile

User = get_user_model()


# MYA START - demo users for guest login
DEMO_USERS = [
    {
        "username": "kevin",
        "email": "kevin@example.com",
        "password": "asdasd24",
        "role": "business",
    },
    {
        "username": "andrey",
        "email": "andrey@example.com",
        "password": "asdasd24",
        "role": "customer",
    },
]


def ensure_demo_users():
    """
    Create fixed demo users for guest login if they do not exist yet.
    """
    for demo_user in DEMO_USERS:
        user, created = User.objects.get_or_create(
            username=demo_user["username"],
            defaults={"email": demo_user["email"]},
        )

        if created:
            user.set_password(demo_user["password"])
            user.save()

        Profile.objects.get_or_create(
            user=user,
            defaults={"role": demo_user["role"]},
        )

        Token.objects.get_or_create(user=user)
# MYA END


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