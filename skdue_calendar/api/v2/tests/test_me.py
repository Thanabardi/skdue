from datetime import datetime, timedelta
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
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
        calendar_slug = generate_slug(self.user.username)
        response = self.client.get(reverse('api_v2:me_calendar', args=[calendar_slug]))
        self.assertEqual(403, response.status_code)

    def test_me_calendar_get_with_not_owner_user(self):
        not_owner_user = User(username="not-owner", password="not-owner")
        not_owner_user.save()
        self.client.force_login(not_owner_user)
        calendar_slug = generate_slug(self.user.username)
        response = self.client.get(reverse('api_v2:me_calendar', args=[calendar_slug]))
        self.assertEqual(403, response.status_code)

    def test_me_calendar_get_with_user(self):
        self.client.force_login(self.user)
        calendar_slug = generate_slug(self.user.username)
        response = self.client.get(reverse('api_v2:me_calendar', args=[calendar_slug]))
        response_data = convert_response(response.content)
        expect = json.dumps({
            "user": UserSerializer(self.user).data,
            "calendar": CalendarSerializer(Calendar.objects.get(slug=calendar_slug)).data,
            "event": {
                "private": CalendarEventSerializer([self.private_event], many=True).data,
                "public": CalendarEventSerializer([self.public_event], many=True).data,
            },
            "tag": ["private", "public"]
        })
        self.assertEqual(expect, response_data)

    def test_me_calendar_get_with_a_follow_calendar(self):
        """Test that api also return followed calendar but not their private events"""
        self.client.force_login(User.objects.get(username="tester"))
        followed = User(username="followed", password="followed")
        followed.save()
        f_calendar = Calendar(
            user=followed,
            name=followed.username,
            slug=generate_slug(followed.username)   
        )
        f_calendar.save()
        f_public_event = CalendarEvent(
            calendar=f_calendar,
            name="f public event",
            slug="f-public-event",
            tag=self.public_tag,
            start_date = self.start_date,
            end_date = self.end_date
        )
        f_public_event.save()
        f_private_event = CalendarEvent(
            calendar=f_calendar,
            name="f private event",
            slug="f-private-event",
            tag=self.private_tag,
            start_date = self.start_date,
            end_date = self.end_date
        )
        f_private_event.save()
        fs = FollowStatus(user=self.user, followed=followed)
        fs.save()
        calendar_slug = generate_slug(self.user.username)
        response = self.client.get(reverse('api_v2:me_calendar', args=[calendar_slug]))
        response_data = convert_response(response.content)
        expect = json.dumps({
            "user": UserSerializer(self.user).data,
            "calendar": CalendarSerializer(Calendar.objects.get(slug=calendar_slug)).data,
            "event": {
                "private": CalendarEventSerializer([self.private_event], many=True).data,
                "public": CalendarEventSerializer([self.public_event, f_public_event], many=True).data,
            },
            "tag": ["private", "public"]
        })
        self.assertEqual(expect, response_data)

    def test_me_calendar_post_with_unlogin(self):
        event_data = {
            "name": self.calendar.name,
            "description": "test event",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tag": self.private_tag.tag
        }
        calendar_slug = self.calendar.slug
        response = self.client.post(reverse('api_v2:me_calendar', args=[calendar_slug]), event_data)
        self.assertEqual(403, response.status_code)

    def test_me_calendar_post_with_a_new_public_event(self):
        self.client.force_login(self.user)
        event_data = {
            "name": "new public test event",
            "description": "test event",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tag": self.public_tag.tag
        }
        calendar_slug = self.calendar.slug
        response = self.client.post(reverse('api_v2:me_calendar', args=[calendar_slug]), data=event_data)
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(CalendarEvent.objects.get(name="new public test event"))

    def test_me_calendar_post_with_a_new_private_event(self):
        self.client.force_login(self.user)
        event_data = {
            "name": "new private test event",
            "description": "test event",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tag": self.private_tag.tag
        }
        calendar_slug = self.calendar.slug
        response = self.client.post(reverse('api_v2:me_calendar', args=[calendar_slug]), data=event_data)
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(CalendarEvent.objects.get(name="new private test event"))

    def test_me_followed_get(self):
        self.client.force_login(User.objects.get(username="tester"))
        followed = User(username="followed", password="followed")
        followed.save()
        fs = FollowStatus(user=self.user, followed=followed)
        response = self.client.get(reverse('api_v2:me_follow'))
        response_data = convert_response(response.content)
        expect = json.dumps(FollowStatusSerializer(FollowStatus.objects.all(), many=True).data)
        self.assertJSONEqual(expect, response_data)

    def test_me_followed_post(self):
        self.client.force_login(User.objects.get(username="tester"))
        followed = User(username="followed", password="followed")
        followed.save()
        response = self.client.post(
            reverse('api_v2:me_follow'),
            data = {
                "option": "follow",
                "follow_id": followed.id}
        )
        self.assertEqual(201, response.status_code)

    def test_me_unfollowed_post(self):
        self.client.force_login(self.user)
        # follow
        followed = User(username="followed", password="followed")
        followed.save()
        self.client.post(
            reverse('api_v2:me_follow'),
            data = {
                "option": "follow",
                "follow_id": followed.id}
        )
        # unfollow
        response = self.client.post(
            reverse('api_v2:me_follow'),
            data = {
                "option": "unfollow",
                "follow_id": followed.id
            }
        )
        with self.assertRaises(FollowStatus.DoesNotExist):
            _ = FollowStatus.objects.get(user=self.user, followed=followed)

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
