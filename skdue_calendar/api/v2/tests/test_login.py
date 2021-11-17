from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import *
from skdue_calendar.models import Calendar


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
        self.calendar1 = Calendar(
            user=self.user1
        )
        self.calendar1.save()

    def test_valid_login(self):
        response = self.client.post(reverse('api_v2:login'), self.user1_account)
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(User.objects.get(username=self.user1_account["username"]).id,
                                            int(self.client.session['_auth_user_id']))
    
    def test_invalid_test(self):
        response = self.client.post(reverse('api_v2:login'), self.user2_account)
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)
