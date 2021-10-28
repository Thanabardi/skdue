from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from .utils import convert_response
import json


def user_data(i):
    return {
        "id": i,
        "username": f"user-{i}",
        "email": f"email-{i}@test.com"
    }


class UserListTests(TestCase):
    def setUp(self):
        self.user_number = 5
        for i in range(1, self.user_number):
            user = User(
                username = f"user-{i}",
                email = f"email-{i}@test.com"
            )
            user.save()

    def test_get(self):
        expected = json.dumps([ user_data(i) for i in range(1, self.user_number) ])
        response = self.client.get(reverse('api_v2:user_list'))
        response_data = convert_response(response.content)
        print(response_data)
        self.assertJSONEqual(expected, response_data)