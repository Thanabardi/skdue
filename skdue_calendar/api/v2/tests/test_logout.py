import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from skdue_calendar import serializers
from .utils import convert_response


class LogoutTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(   "Peem", 
                                            "peem@test.com", 
                                            "peem_pong")
        self.user1.save()
    
    def test_get(self):
        data = {"status": "logged out"}
        expect_data = json.dumps(data)
        response = self.client.get(reverse('api_v2:logout'))
        response_data = convert_response(response.content)
        self.assertJSONEqual(expect_data, response_data)
        