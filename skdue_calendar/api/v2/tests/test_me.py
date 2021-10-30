from datetime import datetime, timedelta
from itertools import chain
import json
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from skdue_calendar.models import *
from skdue_calendar.serializers import *
from skdue_calendar.utils import generate_slug
from .utils import convert_response

class UserMeTests(TestCase):
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
        
        self.user = User(username="tester", password="tester")
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

    def test_me_get_with_login(self):
        self.client.force_login(User.objects.get(username="tester"))
        response = self.client.get(reverse('api_v2:me'))
        response_data = convert_response(response.content)
        expect = json.dumps({
            "user": UserSerializer(self.user).data,
            "calendar": CalendarSerializer([self.calendar], many=True).data,
            "my_custom_tag": [],
            "available_tag": CalendarTagSerializer([self.private_tag, self.public_tag], many=True).data
        })
        self.assertJSONEqual(expect, response_data)

    def test_me_get_with_unlogin(self):
        response = self.client.get(reverse('api_v2:me'))
        self.assertEqual(403, response.status_code)

    def test_me_calendar_get_with_unlogin(self):
        pass

    def test_me_calendar_get_with_not_owner_user(self):
        pass

    def test_me_calendar_get_with_user(self):
        pass

    def test_me_calendar_get_with_a_follow_calendar(self):
        pass

    def test_me_calendar_post(self):
        pass

    def test_me_followed_get(self):
        self.client.force_login(User.objects.get(username="tester"))
        followed = User(username="followed", password="followed")
        followed.save()
        fs = FollowStatus(user=self.user, followed=followed)
        response = self.client.get(reverse('api_v2:me_followed'))
        response_data = convert_response(response.content)
        expect = json.dumps(FollowStatusSerializer(FollowStatus.objects.all(), many=True).data)
        self.assertJSONEqual(expect, response_data)

    def test_me_followed_post(self):
        self.client.force_login(User.objects.get(username="tester"))
        followed = User(username="followed", password="followed")
        followed.save()
        response = self.client.post(
            reverse('api_v2:me_followed'),
            data = {"follow_id": followed.id}
        )
        self.assertEqual(201, response.status_code)

    def test_me_add_tag_post_with_unlogin(self):
        response = self.client.post(reverse('api_v2:me_add_new_tag'), {"tag": "event"})
        self.assertEqual(403, response.status_code)

    def test_me_add_tag_post(self):
        new_tag = "event"
        self.client.force_login(User.objects.get(username="tester"))
        response = self.client.post(reverse('api_v2:me_add_new_tag'), {"tag": new_tag})
        self.assertEqual(200, response.status_code)
        self.assertEqual(new_tag, CalendarTag.objects.get(tag=new_tag).tag)

    def test_me_add_tag_post_with_exist_tag(self):
        new_tag = "public"
        self.client.force_login(User.objects.get(username="tester"))
        response = self.client.post(reverse('api_v2:me_add_new_tag'), {"tag": new_tag})
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, len(CalendarTag.objects.filter(tag=new_tag)))
