import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar
from .utils import convert_response


class CalendarListTests(TestCase):
    def setUp(self):
        user = User(username="tester")
        user.save()
        for i in range(3):
            calendar = Calendar(
                name = f"calendar {i}",
                slug = f"calendar-{i}",
                user = user
            )
            calendar.save()

    def test_get(self):
        """Response is the list of all calendars in JSON form"""
        expect_data = []
        for calendar in Calendar.objects.all():
            data = {
                "id": calendar.id,
                "name": calendar.name,
                "slug": calendar.slug,
                "get_absolute_url": calendar.get_absolute_url(),
                "user": 1
            }
            expect_data.append(data)
        expect_data = json.dumps(expect_data)
        response = self.client.get(reverse('api_v2:calendar_list'))
        response_data = convert_response(response.content)
        self.assertJSONEqual(expect_data, response_data)

    def test_post_with_invalid_event_data(self):
        """Response is the fail status with message"""
        # TODO: add this test case after implement new `is_valid` method in `Calendar` model
        # what to test status_code, resounse_data
        pass

    def test_post_with_valid_calendar_data(self):
        """Response is the new calendar data with success status"""
        # TODO: add this test case after implement new `is_valid` method in `Calendar` model
        # what to test status_code, resounse_data
        pass
