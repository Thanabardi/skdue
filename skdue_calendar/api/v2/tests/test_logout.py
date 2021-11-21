import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from skdue_calendar import serializers
from .utils import convert_response, authenticated_client_factory
from rest_framework.authtoken.models import Token
class LogoutTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(   "Peem", 
                                            "peem@test.com", 
                                            "peem_pong")
        self.user1.save()
    
    def test_get(self):
        self.client = authenticated_client_factory(self.user1)
        response = self.client.delete(reverse('api_v2:logout'))
        response_data = convert_response(response.content)
        with self.assertRaises(Token.DoesNotExist):
            _ = Token.objects.get(user=self.user1)
    