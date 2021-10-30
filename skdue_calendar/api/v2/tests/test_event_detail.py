import json
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from skdue_calendar.models import *
from skdue_calendar.serializers import *
from skdue_calendar.utils import generate_slug
from .utils import convert_response


class EventDetailTests(TestCase):
    def setUp(self):
        self.start_date = datetime.now().replace(microsecond=0)
        self.end_date = self.start_date + timedelta(days=1)

        tag = CalendarTagType(tag_type="default")
        tag.save()
        self.DEFAULT_TAG_TYPE = CalendarTagType.objects.get(tag_type="default")

        tag = CalendarTagType(tag_type="private")
        tag.save()
        self.PRIVATE_TAG_TYPE = CalendarTagType.objects.get(tag_type="private")

        tag = CalendarTagType(tag_type="custom")
        tag.save()
        self.CUSTOM_TAG_TYPE = CalendarTagType.objects.get(tag_type="custom")
        
        self.user = User(username="tester")
        self.user.save()
        self.calendar = Calendar(
            user=self.user,
            name=self.user.username,
            slug=generate_slug(self.user.username)    
        )
        self.calendar.save()
        self.public_tag = CalendarTag(
            user=self.user,
            tag="public",
            tag_type=self.DEFAULT_TAG_TYPE,
        )
        self.public_tag.save()
        self.public_event = CalendarEvent(
            calendar=self.calendar,
            name="public event",
            slug="public-event",
            tag=self.public_tag,
            start_date = self.start_date,
            end_date = self.end_date
        )
        self.public_event.save()
        self.private_tag = CalendarTag(
            user=self.user,
            tag="private",
            tag_type=self.PRIVATE_TAG_TYPE
        )
        self.private_tag.save()
        self.private_event = CalendarEvent(
            calendar=self.calendar,
            name="private event",
            slug="private-event",
            tag=self.private_tag,
            start_date = self.start_date,
            end_date = self.end_date
        )
        self.private_event.save()  

    def test_get_exist_event(self):
        """Test that api return right event"""    
        calendar_slug = self.calendar.slug
        event_slug = self.public_event.slug
        response = self.client.get(reverse('api_v2:event_detail', args=[calendar_slug, event_slug]))
        response_data = convert_response(response.content)
        expect = json.dumps(CalendarEventSerializer(self.public_event).data)
        self.assertJSONEqual(expect, response_data)

    def test_get_non_exist_event(self):
        """Test that api return 404"""
        calendar_slug = self.calendar
        event_slug = "not-exist-event"
        response = self.client.get(reverse('api_v2:event_detail', args=[calendar_slug, event_slug]))
        self.assertEqual(404, response.status_code)

    def test_get_non_exist_calendar(self):
        """Test that api return 404"""
        calendar_slug = "not-exist-calendar"
        event_slug = "not-exist-event"
        response = self.client.get(reverse('api_v2:event_detail', args=[calendar_slug, event_slug]))
        self.assertEqual(404, response.status_code)

    def test_get_private_event(self):
        """Test that API does not allow people to get private event"""
        calendar_slug = self.calendar.slug
        event_slug = self.private_event.slug
        response = self.client.get(reverse('api_v2:event_detail', args=[calendar_slug, event_slug]))
        self.assertEqual(403, response.status_code)