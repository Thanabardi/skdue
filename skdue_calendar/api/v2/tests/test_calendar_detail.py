import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import *
from skdue_calendar.serializers import *
from skdue_calendar.utils import generate_slug
from .utils import convert_response


class CalendarDetailTests(TestCase):
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

    def test_get(self):
        """Test that calendar detail does not show private events."""
        calendar_slug = self.calendar.slug
        response = self.client.get(reverse('api_v2:calendar_detail', args=[calendar_slug]))
        response_data = convert_response(response.content)
        expect = json.dumps({
            "user": UserSerializer(self.user).data,
            "calendar": CalendarSerializer(self.calendar).data,
            "event": {
                str(self.public_tag.tag): CalendarEventSerializer([self.public_event], many=True).data,
            },
            "tag": [self.public_tag.tag]
        })
        self.assertJSONEqual(expect, response_data)
