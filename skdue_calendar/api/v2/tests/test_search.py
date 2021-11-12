from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from skdue_calendar.models import *
from skdue_calendar.serializers.calendar_event_serializer import CalendarEventSerializer
from skdue_calendar.serializers.calendar_serializer import CalendarSerializer
from skdue_calendar.serializers.calendar_tag_serializer import CalendarTagSerializer
from skdue_calendar.utils import generate_slug
from .utils import convert_response
import json


class SearchTests(TestCase):
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
            tag=self.private_tag,
            start_date = self.start_date,
            end_date = self.end_date
        )
        self.private_event.save()

    def test_get(self):
        """Test that search returns all public data"""
        response = self.client.get(reverse('api_v2:search'))
        response_data = convert_response(response.content)
        expect = json.dumps({
            "calendar": CalendarSerializer([self.calendar], many=True).data,
            "event": CalendarEventSerializer([self.public_event], many=True).data,
            "tag": CalendarTagSerializer([self.public_tag], many=True).data
        })
        self.assertJSONEqual(expect, response_data)
