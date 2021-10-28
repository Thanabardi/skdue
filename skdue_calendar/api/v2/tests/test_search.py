from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.http import response
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.utils.translation import deactivate_all
from skdue_calendar.models import *
from skdue_calendar.utils import generate_slug
from .utils import convert_response
import json


class SearchTests(TestCase):
    def setUp(self):
        self.user_num = 5
        self.start_date = datetime.now().replace(microsecond=0)
        self.end_date = self.start_date + timedelta(days=1)
        for i in range(1, self.user_num):
            user = User(
                username = f"user-{i}",
                email = f"user-{i}@test.com"
            )
            user.save()
            calendar = Calendar(
                name = user.username,
                slug = generate_slug(user.username),
                user = user
            )
            tag = CalendarTag(user=user, tag=f"tag-{i}")
            tag.save()
            calendar.save()
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

    def tag_data(self, i):
        return {
            "id": i,
            "tag": f"tag-{i}",
            "user": i
        }

    def calendar_data(self, i):
            return {
                "id": i,
                "name": f"user-{i}",
                "slug": f"user-{i}",
                "get_absolute_url": f"/user-{i}",
                "user": i
            }

    def event_data(self, i):
            return {
                "id": i,
                "calendar": i,
                "name": f"event {i}",
                "slug": f"event-{i}",
                "get_absolute_url": f"/user-{i}/event-{i}",
                "description": f"desc event {i}",
                "start_date": self.start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "end_date": self.end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "tag_text": f"tag-{i}" 
            }

    def test_get(self):
        expect = json.dumps({
            "calendar": [ self.calendar_data(i) for i in range(1, self.user_num) ],
            "event": [ self.event_data(i) for i in range(1, self.user_num) ],
            "tag": [ self.tag_data(i) for i in range(1, self.user_num)]
        })
        response = self.client.get(reverse('api_v2:search'))
        response_data = convert_response(response.content)
        self.assertJSONEqual(expect, response_data)