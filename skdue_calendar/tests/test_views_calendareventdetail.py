import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from skdue_calendar.models import Calendar, CalendarEvent

def convert_response(data):
    """Convert data to the same JSON format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data

class CalendarEventDetailViewTests(TestCase):
    def setUp(self):
        self.start_date = datetime.now().replace(microsecond=0)
        self.end_date = self.start_date + timedelta(days=1)
        calendar = Calendar(name="calendar", slug="calendar")
        calendar.save()
        for i in range(3):
            event = CalendarEvent(
                calendar = calendar,
                name = f"event {i}",
                slug = f"event-{i}",
                description = f"desc for event {i}",
                start_date = self.start_date,
                end_date = self.end_date
            )
            event.save()

    def test_get_object_not_found_from_not_exist_calendar(self):
        """Raise 404 when calendar does not exist"""
        calendar_slug = "not-exist-calendar"
        event_slug = "event-0"
        response = self.client.get(reverse('skdue_calendar:event_detail', args=[calendar_slug, event_slug]))
        self.assertEqual(404, response.status_code)

    def test_get_object_not_fount_from_not_exist_event(self):
        """Raise 404 when event does not exist"""
        calendar_slug = "calendar"
        event_slug = "not-exist-event"
        response = self.client.get(reverse('skdue_calendar:event_detail', args=[calendar_slug, event_slug]))
        self.assertEqual(404, response.status_code)

    def test_get(self):
        """Returns detail of event"""
        calendar_slug = "calendar"
        event_slug = "event-0"
        response = self.client.get(reverse('skdue_calendar:event_detail', args=[calendar_slug, event_slug]))
        response_data = convert_response(response.content)
        expect = json.dumps({
            "id": 1,
            "name": "event 0",
            "slug": "event-0",
            "get_absolute_url": "/calendar/event-0",
            "description": "desc for event 0",
            "start_date": self.start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "end_date": self.end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        })
        self.assertJSONEqual(expect, response_data)