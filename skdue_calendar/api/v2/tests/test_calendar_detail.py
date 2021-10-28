import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar, CalendarEvent, CalendarTag
from .utils import convert_response


class CalendarDetailTests(TestCase):
    def setUp(self):
        self.start_date = datetime.now().replace(microsecond=0)
        self.end_date = self.start_date + timedelta(days=1)
        user = User(username="tester")
        user.save()
        calendar = Calendar(
            name = "calendar",
            slug = "calendar",
            user = user
        )
        calendar.save()
        tag = CalendarTag(user=user, tag="event")
        tag.save()
        for i in range(3):
            event = CalendarEvent(
                calendar = calendar,
                name = f"event {i}",
                slug = f"event-{i}",
                description = f"desc event {i}",
                start_date = self.start_date,
                end_date = self.end_date,
                tag = tag
            )
            event.save()

    def test_get_object_not_found(self):
        """Response code is 404 when calendar does not exist"""
        calendar_slug = "not-exist-calendar"
        response = self.client.get(reverse('api_v2:calendar_detail', args=[calendar_slug]))
        self.assertEqual(404, response.status_code)

    def test_get(self):
        calendar_slug = "calendar"
        response = self.client.get(reverse('api_v2:calendar_detail', args=[calendar_slug]))
        response_data = convert_response(response.content)
        expects = []
        for i in range(3):
            expects.append({
                "id": i+1,
                "calendar": 1,
                "name": f"event {i}",
                "slug": f"event-{i}",
                "get_absolute_url": f"/calendar/event-{i}",
                "description": f"desc event {i}",
                "start_date": self.start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "end_date": self.end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "tag_text": "event"
            })
        expects = json.dumps(expects)
        self.assertJSONEqual(expects, response_data)

    def test_post_with_invalid_event_data(self):
        """Response is the fail status with message"""
        # TODO: add this test case after implement new `is_valid` method in `Calendar` model
        # what to test status_code, resounse_data
        pass

    def test_post_with_valid_event_data(self):
        """Response is the new event data with success status"""
        # TODO: add this test case after implement new `is_valid` method in `Calendar` model
        # what to test status_code, resounse_data
        pass