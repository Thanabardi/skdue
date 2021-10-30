import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar
from skdue_calendar.serializers import CalendarSerializer
from skdue_calendar.utils import generate_slug
from .utils import convert_response


class CalendarListTests(TestCase):
    def setUp(self):
        self.user = User(username="tester")
        self.user.save()
        self.calendar = Calendar(
            user=self.user,
            name=self.user.username,
            slug=generate_slug(self.user.username)
        )
        self.calendar.save()

    def test_get(self):
        response = self.client.get(reverse('api_v2:calendar_list'))
        response_data = convert_response(response.content)
        expect = json.dumps(CalendarSerializer([self.calendar], many=True).data)
        self.assertJSONEqual(expect, response_data)