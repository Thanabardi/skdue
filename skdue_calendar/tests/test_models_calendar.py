from django.test import TestCase
from skdue_calendar.models import Calendar


class CalendarModelTests(TestCase):
    def setUp(self):
        self.calendars = []
        self.calendars.append(Calendar(name="calendar 1", slug="calendar-1"))
        self.calendars.append(Calendar(name="calendar 2", slug="calendar-2"))
        # save in TestCase does not apply to real database
        for calendar in self.calendars:
            calendar.save()

    def test_valid_arguments(self):
        """Test that arguments are correct, and number of calendar is equal to number of created calendar"""
        expects = [
            {
                "name": "calendar 1",
                "slug": "calendar-1"
            },
            {
                "name": "calendar 2",
                "slug": "calendar-2"
            }
        ]
        for expect, calendar in zip(expects, Calendar.objects.all()):
            with self.subTest():
                self.assertEqual(expect["name"], calendar.name)
            with self.subTest():
                self.assertEqual(expect["slug"], calendar.slug)
        with self.subTest():
            self.assertEqual(2, len(Calendar.objects.all()))

    def test_invalid_calendar_data(self):
        """Returns false for new calendar data that calendar slug already exist"""
        calendar_data = {
            "name": "calendar 1"
        }
        self.assertFalse(Calendar.is_valid(calendar_data))

    def test_valid_calendar_data(self):
        """Returns true for new calendar data that calendar slug does not exist"""
        calendar_data = {
            "name": "calendar 3"
        }
        self.assertTrue(Calendar.is_valid(calendar_data))

    def test_get_absolute_url(self):
        """Absolute url is valid"""
        expects = ["/calendar-1", "/calendar-2"]
        for calendar, expect in zip(Calendar.objects.all(), expects):
            with self.subTest():
                self.assertEqual(expect, calendar.get_absolute_url())
                