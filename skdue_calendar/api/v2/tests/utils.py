import json
from rest_framework.authtoken.models import Token
from django.test import Client
from django.contrib.auth.models import User

def convert_response(data):
    """Convert data to the same JSON format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data

def autenticated_client_factory(user: User) -> Client:
    """Return client with autentication token"""
    token, _ = Token.objects.get_or_create(user=user)
    return Client(HTTP_AUTHORIZATION='Token ' + token.key)