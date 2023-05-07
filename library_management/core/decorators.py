from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .tokens import *
from django.shortcuts import render

def token_validator(view_function):
    def decorator(request, *args, **kwargs):
        if not request.COOKIES.get("jwt_token"):
            return render(request, 'auth_error.html', {'error_msg': "unauthenticated, jwt token not found in request"})

        user_id = decode_jwt_token(
            request.COOKIES.get("jwt_token"),request
        )
        if not isinstance(user_id ,int):
            return user_id
            
        request.META['user_id'] = user_id
        
        return view_function(request, *args, **kwargs)
    
    return decorator