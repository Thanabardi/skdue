from datetime import datetime, timedelta
from django.contrib.auth.models import User

from django.test import TestCase
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar, CalendarEvent, CalendarTag, CalendarTagType
from skdue_calendar.utils import generate_slug


class CalendarTagModelTests(TestCase):
    def setUp(self):
        self.start_date = datetime.now().replace(microsecond=0)
        user = User(username="tester")
        user.save()
        tag_type = CalendarTagType(tag_type="default")
        tag_type.save()
        self.tag = CalendarTag(user=user, tag="event", tag_type=tag_type)
        self.tag.save()
        for i in range(3):
            name = f"calendar {i}"
            slug = generate_slug(name)
            calendar = Calendar(name=name, slug=slug, user=user)
            calendar.save()

    def test_invalid_tag_with_same_name_in_same_calendar(self):
        """Test that tag will can't create"""
        calendar_1 = Calendar.objects.get(slug="calendar-1")
        old_event = CalendarEvent(
            calendar = calendar_1,
            name = "old event",
            slug = "old-event",
            start_date = self.start_date,
            end_date = self.start_date + timedelta(days=1),
            tag = self.tag
        )
        old_event.save()
        new_event_data = {
          "name": "old event",
          "start_date": str(self.start_date),
          "end_date": str(self.start_date + timedelta(days=1)),
          "tag_text": str(self.tag)
        }
        self.assertFalse(CalendarTag.is_valid(new_event_data, "calendar-1"))

    def test_valid_tag(self):
        """Test that tag can create"""
        calendar_1 = Calendar.objects.get(slug="calendar-1")
        old_event = CalendarEvent(
            calendar = calendar_1,
            name = "old event",
            slug = "old-event",
            start_date = self.start_date,
            end_date = self.start_date + timedelta(days=1),
            tag = self.tag
        )
        old_event.save()
        new_event_data = {
          "name": "new event",
          "start_date": str(self.start_date),
          "end_date": str(self.start_date + timedelta(days=1)),
          "tag_text": str(self.tag)
        }
        self.assertTrue(CalendarTag.is_valid(new_event_data, "calendar-2"))
    
    def test_valid_tag_in_same_calendar(self):
        """Test that tag can create in the same calendar"""
        calendar_1 = Calendar.objects.get(slug="calendar-1")
        old_event = CalendarEvent(
            calendar = calendar_1,
            name = "old event",
            slug = "old-event",
            start_date = self.start_date,
            end_date = self.start_date + timedelta(days=1),
            tag = self.tag
        )
        old_event.save()
        new_event_data = {
          "name": "new event",
          "start_date": str(self.start_date),
          "end_date": str(self.start_date + timedelta(days=1)),
          "tag_text": "halloween"
        }
        self.assertTrue(CalendarTag.is_valid(new_event_data, "calendar-1"))