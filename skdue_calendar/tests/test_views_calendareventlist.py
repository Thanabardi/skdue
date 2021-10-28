import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar, CalendarEvent, CalendarTag

def convert_response(data):
    """Convert data to the same JSON format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data

class CalendarEventListTests(TestCase):
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
        response = self.client.get(reverse('skdue_calendar:event_list', args=[calendar_slug]))
        self.assertEqual(404, response.status_code)

    def test_get(self):
        calendar_slug = "calendar"
        response = self.client.get(reverse('skdue_calendar:event_list', args=[calendar_slug]))
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
                # TODO: change tag_text value after create Tag model and edit CalendarEvent model
                "tag_text": "event"
            })
        expects = json.dumps(expects)
        self.assertJSONEqual(expects, response_data)

    def test_post_with_invalid_event_data(self):
        calendar_slug = "calendar"
        start_date = datetime.now().replace(microsecond=0)
        end_date = start_date - timedelta(days=1)
        data = {
            "name": "invalid event",
            "description": "desc for invalid event",
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
        response = self.client.post(reverse('skdue_calendar:event_list', args=[calendar_slug]), data)
        response_data = convert_response(response.content)
        expect = json.dumps({
            "status": "failed",
            "msg": "invalid calendar event"
        })
        with self.subTest():
            self.assertJSONEqual(expect, response_data)
        # post request does not create new event
        with self.subTest():
            events = CalendarEvent.objects.filter(calendar__slug=calendar_slug)
            self.assertEqual(3, len(events))

    def test_post_with_valid_event_data(self):
        calendar_slug = "calendar"
        data = {
            "name": "valid event",
            "description": "desc for valid event",
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "tag": "event"
        }
        response = self.client.post(reverse('skdue_calendar:event_list', args=[calendar_slug]), data)
        response_data = convert_response(response.content)
        expect = json.dumps({
            "id": 4,
            "calendar": 1,
            "name": "valid event",
            "slug": "valid-event",
            "get_absolute_url": "/calendar/valid-event",
            "description": "desc for valid event",
            "start_date": self.start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "end_date": self.end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            # TODO: change tag_text value after create Tag model and edit CalendarEvent model
            "tag_text": "event",
            "status": "success",
            "msg": "calendar event created"
        })
        with self.subTest():
            self.assertJSONEqual(expect, response_data)
        # post request create new event in calendar
        with self.subTest():
            event = CalendarEvent.objects.get(slug="valid-event")
            self.assertEqual("valid event", str(event))