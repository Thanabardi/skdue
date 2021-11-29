import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User

def convert_response(data):
    """Convert data to the same JSON format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data

def authenticated_client_factory(user: User) -> APIClient:
    """Return client with autentication token"""
    token, _ = Token.objects.get_or_create(user=user)
    return APIClient(HTTP_AUTHORIZATION='Token ' + token.key)