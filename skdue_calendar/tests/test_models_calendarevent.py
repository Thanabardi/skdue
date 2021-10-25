from datetime import datetime, timedelta

from django.test import TestCase
from skdue_calendar.models import Calendar, CalendarEvent
from skdue_calendar.utils import generate_slug


class CalendarEventModelTests(TestCase):
    def setUp(self):
        self.start_date = datetime.now().replace(microsecond=0)
        for i in range(3):
            name = f"calendar {i}"
            slug = generate_slug(name)
            calendar = Calendar(name=name, slug=slug)
            calendar.save()

    def test_invalid_event_when_calendar_not_found(self):
        """Test that is_valid will return False when calendar not found"""
        new_event_data = {
            "name": "old event",
            "start_date": str(self.start_date),
            "end_date": str(self.start_date + timedelta(days=1))
        }
        # validate with same name but different calendar
        self.assertFalse(CalendarEvent.is_valid(new_event_data, "calendar"))

    def test_invalid_event_with_invalid_date(self):
        """Test that is_valid will return False when start date >= end date"""
        end_date_interval = [timedelta(days=1), timedelta(seconds=1)]
        for interval in end_date_interval:
            new_event = {
                "name": "test event",
                "start_date": str(self.start_date),
                "end_date": str(self.start_date - interval)
            }
            with self.subTest():
                self.assertFalse(CalendarEvent.is_valid(new_event, "calendar-0"), interval)
    
    def test_invalid_event_with_same_name_in_same_calendar(self):
        """Test that is_valid will return False when name is invalid.
        New name is avaliable when the event name already exist in the same calendar.
        """
        # old event
        calendar_1 = Calendar.objects.get(slug="calendar-1")
        old_event = CalendarEvent(
            calendar = calendar_1,
            name = "old event",
            slug = "old-event",
            start_date = self.start_date,
            end_date = self.start_date + timedelta(days=1)
        )
        old_event.save()
        new_event_data = {
            "name": "old event",
            "start_date": str(self.start_date),
            "end_date": str(self.start_date + timedelta(days=1))
        }
        # validate with same name but different calendar
        self.assertFalse(CalendarEvent.is_valid(new_event_data, "calendar-1"))

    def test_valid_event_with_valid_date(self):
        """Test that is_valid will return True when start date < end date"""
        end_date_interval = [timedelta(days=1), timedelta(seconds=1)]
        for interval in end_date_interval:
            new_event = {
                "name": "test event",
                "start_date": str(self.start_date),
                "end_date": str(self.start_date + interval)
            }
            with self.subTest():
                self.assertTrue(CalendarEvent.is_valid(new_event, "calendar-0"), interval)

    def test_valid_event_with_same_name_in_diffent_calendar(self):
        """Test that is_valid will return True when name is valid.
        New name is avaliable when the event name is not exist in the same calendar."""
        # old event
        calendar_1 = Calendar.objects.get(slug="calendar-1")
        old_event = CalendarEvent(
            calendar = calendar_1,
            name = "old event",
            slug = "old-event",
            start_date = self.start_date,
            end_date = self.start_date + timedelta(days=1)
        )
        old_event.save()
        new_event_data = {
            "name": "old event",
            "start_date": str(self.start_date),
            "end_date": str(self.start_date + timedelta(days=1))
        }
        # validate with same name but different calendar
        self.assertTrue(CalendarEvent.is_valid(new_event_data, "calendar-2"))

    def test_get_absolute_url(self):
        """Test that get_absolute_url returns correct url"""
        for i in range(3):
            calendar = Calendar.objects.get(slug=f"calendar-{i}")
            with self.subTest():
                event = CalendarEvent(
                    calendar = calendar,
                    name = f"event {i}",
                    slug = f"event-{i}",
                    start_date = self.start_date,
                    end_date = self.start_date + timedelta(days=1)
                )
                self.assertEqual(f"/calendar-{i}/event-{i}", event.get_absolute_url())
