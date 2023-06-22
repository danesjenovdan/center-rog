from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta

from users.models import BookingToken


def get_email_for_token(token):
    # check if token exists and is not older than 120 minutes
    booking_token = BookingToken.objects.filter(
        token=token,
        created__gte=timezone.now() - timedelta(minutes=120)
    ).first()

    # if token exists, return the email
    if booking_token:
        return booking_token.email

    # otherwise, return None
    return None

def get_token_for_user(user):
    # check if token exists for this user and is not older than 60 minutes
    booking_token = BookingToken.objects.filter(
        email=user.email,
        created__gte=timezone.now() - timedelta(minutes=60)
    ).first()

    # if token exists, return it
    if booking_token:
        return booking_token.token

    # otherwise, delete all tokens for this user and create a new one
    BookingToken.objects.filter(email=user.email).delete()
    token = get_random_string(length=32)
    booking_token = BookingToken.objects.create(email=user.email, token=token)
    return booking_token.token
