import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls.base import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar, CalendarEvent, CalendarTag, CalendarTagType


def convert_response(data):
    """Convert data to the same JSON format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data


class SearchViewTests(TestCase):
    def setUp(self):
        self.start_date = datetime.now().replace(microsecond=0)
        self.end_date = self.start_date + timedelta(days=1)
        user = User(username="tester")
        user.save()
        tag_type = CalendarTagType(tag_type="default")
        tag_type.save()
        tag = CalendarTag(user=user, tag="event", tag_type=tag_type)
        tag.save()
        for i in range(3):
            calendar = Calendar(
                name = f"calendar {i}",
                slug = f"calendar-{i}",
                user = user
            )
            calendar.save()
        for i in range(3):
            event = CalendarEvent(
                calendar = Calendar.objects.get(slug=f"calendar-{i}"),
                name = f"event {i}",
                slug = f"event-{i}",
                description = f"desc event {i}",
                start_date = self.start_date,
                end_date = self.end_date,
                tag = tag
            )
            event.save()

    def event_data(self, i):
        return {
            "id": i+1,
            "calendar": i+1,
            "name": f"event {i}",
            "slug": f"event-{i}",
            "get_absolute_url": f"/calendar-{i}/event-{i}",
            "description": f"desc event {i}",
            "start_date": self.start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "end_date": self.end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "tag_text": "event" 
        }

    def calendar_data(self, i):
        return {
            "id": i+1,
            "name": f"calendar {i}",
            "slug": f"calendar-{i}",
            "get_absolute_url": f"/calendar-{i}",
            "user": 1
        }

    def test_get(self):
        expect = json.dumps({
            "calendar": [self.calendar_data(i) for i in range(3)],
            "event": [self.event_data(i) for i in range(3)],
        })
        response = self.client.get(reverse('skdue_calendar:search'))
        response_data = json.dumps(response.data)
        self.assertJSONEqual(expect, response_data)
