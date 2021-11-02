import json
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .utils import convert_response


class LoginTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(   "Past", 
                                            "past@test.com", 
                                            "past1234")
        self.user1.save()
        self.user1_account = {  "username":"Past",
                                "email":"past@test.com",
                                "password":"past1234"
                            }
        self.user2_account = {  "username":"Pastpong",
                                "email":"pastpong@test.com",
                                "password":"pastpong1234"
                            }

    def test_valid_login(self):
        response = self.client.post(reverse('api_v2:login'), self.user1_account)
        self.assertEqual(200, response.status_code)
    
    def test_invalid_test(self):
        response = self.client.post(reverse('api_v2:login'), self.user2_account)
        self.assertEqual(404, response.status_code)
        
