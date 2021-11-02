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
        self.tag_type = CalendarTagType(tag_type="default")
        self.tag_type.save()
        self.tag = CalendarTag(user=user, tag="event", tag_type=self.tag_type)
        self.tag.save()
        for i in range(3):
            name = f"calendar {i}"
            slug = generate_slug(name)
            calendar = Calendar(name=name, slug=slug, user=user)
            calendar.save()

    def test_tag_type(self):
        self.assertEqual(self.tag_type.tag_type, self.tag.tag_type_text)

    def test_is_valid_with_valid_tag(self):
        """Test that a is_valid return True for not exist tag"""
        data = {"tag": "new_tag"}
        self.assertTrue(CalendarTag.is_valid(data))

    def test_is_valid_with_exist_tag(self):
        """"Test that is_valid return False for exist tag"""
        data = {"tag": self.tag.tag}
        self.assertFalse(CalendarTag.is_valid(data))