from rest_framework.authtoken.models import Token
from profiles_app.models import Profile


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