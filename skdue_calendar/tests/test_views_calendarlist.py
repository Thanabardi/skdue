import json
from django.test import TestCase
from django.urls import reverse
from skdue_calendar.models import Calendar

def convert_response(data):
    """Convert data to the same JSON format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data

class CalendarListViewTests(TestCase):
    def setUp(self):
        for i in range(3):
            calendar = Calendar(
                name = f"calendar {i}",
                slug = f"calendar-{i}"
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
                "get_absolute_url": calendar.get_absolute_url()
            }
            expect_data.append(data)
        expect_data = json.dumps(expect_data)
        response = self.client.get(reverse('skdue_calendar:list'))
        response_data = convert_response(response.content)
        self.assertJSONEqual(expect_data, response_data)

    def test_post_with_invalid_event_data(self):
        """Response is the fail status with message"""
        # data of already exist calendar
        data = {"name": "calendar 0"}
        response = self.client.post(reverse('skdue_calendar:list'), data)
        response_data = convert_response(response.content)
        expect = json.dumps({"status": "failed", "msg": "invalid calendar"})
        with self.subTest():
            self.assertJSONEqual(expect, response_data)
        # post request does not create new calendar
        with self.subTest():
            calendar = Calendar.objects.filter(name=data["name"])
            self.assertEqual(1, len(calendar))

    def test_post_with_valid_calendar_data(self):
        """Response is the new calendar data with success status"""
        data = {"name": "calendar 3"}
        response = self.client.post(reverse('skdue_calendar:list'), data)
        response_data = convert_response(response.content)
        expect = json.dumps({
            "id": 4,
            "name": "calendar 3",
            "slug": "calendar-3",
            "get_absolute_url": "/calendar-3",
            "status": "success",
            "msg": "calendar created"
        })
        with self.subTest():
            self.assertJSONEqual(expect, response_data)
        # post request create new calendar
        with self.subTest():
            calendar = Calendar.objects.get(name=data["name"])
            self.assertEqual(data["name"], str(calendar))
