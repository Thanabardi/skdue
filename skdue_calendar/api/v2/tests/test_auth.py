import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import *
from .utils import convert_response


class GetAuthTokenTest(TestCase):
    def setUp(self):
        self.username = "tester"
        self.password = "tester_pwd"
        self.user = User(username=self.username, password=self.password)
        self.user.save()
        self.token = Token(user=self.user)
        self.token.save()

    def test_post(self):
        """Test that user get their token after they request it"""
        response = self.client.post(
            path=reverse('api_v2:get_auth_token'),
            data={"username": self.username, "password": self.password})
        response_data = convert_response(response.content)
        expect = json.dumps({"token": self.token})
        self.assertJSONEqual(expect, response_data)

    def test_post(self):
        """Test that no token return whenever login data is invalid"""
        response = self.client.post(
            path=reverse('api_v2:get_auth_token'),
            data={"username": self.user, "password": "imposter_pwd"}
        )
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)