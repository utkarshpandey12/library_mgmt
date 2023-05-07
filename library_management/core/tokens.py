import datetime
from datetime import timedelta

import jwt
from django.utils import timezone
from rest_framework import exceptions
from django.shortcuts import render



def create_jwt_token(user_id):
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=240)
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": expiry_time,
        },
        "refresh_token_secret",
        algorithm="HS256",
    )

    return token


def decode_jwt_token(token,request):
    try:
        payload = jwt.decode(token, "refresh_token_secret", algorithms="HS256")
        return payload["user_id"]
    except Exception:
        return render(request, 'auth_error.html', {'error_msg': "Unauthenticated, invalid jwt token!"})