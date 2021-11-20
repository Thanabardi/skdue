from datetime import datetime, timedelta
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import *
from skdue_calendar.models import *
from skdue_calendar.serializers import *
from skdue_calendar.utils import generate_slug
from .utils import convert_response, authenticated_client_factory


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

        # other user
        self.other = User(username="other", password="other_pwd")
        self.other.save()

        self.other_calendar = Calendar(
            user=self.other,
            name=self.other.username,
            slug=generate_slug(self.other.username)
        )
        self.other_calendar.save()

        self.other_tag = CalendarTag(
            user=self.other,
            tag="other",
            tag_type=self.CUSTOM_TAG_TYPE
        )
        self.other_tag.save()

        self.other_event = CalendarEvent(
            calendar=self.other_calendar,
            name="other event",
            slug="other-event",
            tag=self.other_tag,
            start_date = self.start_date,
            end_date = self.end_date
        )

    def test_me_get_with_login(self):
        self.client = authenticated_client_factory(self.user)
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
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_me_calendar_get_with_unlogin(self):
        calendar_slug = generate_slug(self.user.username)
        response = self.client.get(reverse('api_v2:me_calendar', args=[calendar_slug]))
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_me_calendar_get_with_not_owner_user(self):
        not_owner_user = User(username="not-owner", password="not-owner")
        not_owner_user.save()
        self.client = authenticated_client_factory(not_owner_user)
        calendar_slug = generate_slug(self.user.username)
        response = self.client.get(reverse('api_v2:me_calendar', args=[calendar_slug]))
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_me_calendar_get_with_user(self):
        self.client = authenticated_client_factory(self.user)
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
        self.client = authenticated_client_factory(self.user)
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
        fs = FollowStatus(user=self.user, followed=followed, followed_calendar=f_calendar)
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
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_me_calendar_post_with_a_new_public_event(self):
        self.client = authenticated_client_factory(self.user)
        event_data = {
            "name": "new public test event",
            "description": "test event",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tag": self.public_tag.tag
        }
        calendar_slug = self.calendar.slug
        response = self.client.post(reverse('api_v2:me_calendar', args=[calendar_slug]), data=event_data)
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(CalendarEvent.objects.get(name="new public test event"))

    def test_me_calendar_post_with_a_new_private_event(self):
        self.client = authenticated_client_factory(self.user)
        event_data = {
            "name": "new private test event",
            "description": "test event",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tag": self.private_tag.tag
        }
        calendar_slug = self.calendar.slug
        response = self.client.post(reverse('api_v2:me_calendar', args=[calendar_slug]), data=event_data)
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(CalendarEvent.objects.get(name="new private test event"))

    def test_me_followed_get(self):
        self.client = authenticated_client_factory(self.user)
        followed = User(username="followed", password="followed")
        followed.save()
        followed_cal = Calendar(
            user=followed,
            name=followed.username,
            slug=generate_slug(followed.username)
        )
        followed_cal.save()
        fs = FollowStatus(user=self.user, followed=followed, followed_calendar=followed_cal)
        response = self.client.get(reverse('api_v2:me_follow'))
        response_data = convert_response(response.content)
        expect = json.dumps(FollowStatusSerializer(FollowStatus.objects.all(), many=True).data)
        self.assertJSONEqual(expect, response_data)

    def test_me_followed_post(self):
        self.client = authenticated_client_factory(self.user)
        followed = User(username="followed", password="followed")
        followed.save()
        calendar = Calendar(
            user=followed,
            name=followed.username,
            slug=generate_slug(followed.username)
        )
        calendar.save()
        response = self.client.post(
            reverse('api_v2:me_follow'),
            data = {
                "option": "follow",
                "follow_id": followed.id,
                "follow_calendar": calendar.id
                }
        )
        self.assertEqual(HTTP_201_CREATED, response.status_code)

    def test_me_unfollowed_post(self):
        self.client = authenticated_client_factory(self.user)

        # follow
        followed = User(username="followed", password="followed")
        followed.save()
        calendar = Calendar(
            user=followed,
            name=followed.username,
            slug=generate_slug(followed.username)
        )
        calendar.save()
        self.client.post(
            reverse('api_v2:me_follow'),
            data = {
                "option": "follow",
                "follow_id": followed.id,
                "follow_calendar": calendar.id,
            }
        )
        # unfollow
        response = self.client.post(
            reverse('api_v2:me_follow'),
            data = {
                "option": "unfollow",
                "follow_id": followed.id,
                "follow_calendar": calendar.id,
            }
        )
        with self.assertRaises(FollowStatus.DoesNotExist):
            _ = FollowStatus.objects.get(user=self.user, followed=followed)

    def test_me_add_tag_post_with_unlogin(self):
        response = self.client.post(reverse('api_v2:me_add_new_tag'), {"tag": "event"})
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_me_add_tag_post(self):
        new_tag = "event"
        self.client = authenticated_client_factory(self.user)
        response = self.client.post(reverse('api_v2:me_add_new_tag'), {"tag": new_tag})
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertEqual(new_tag, CalendarTag.objects.get(tag=new_tag).tag)

    def test_me_add_tag_post_with_exist_tag(self):
        new_tag = "public"
        self.client = authenticated_client_factory(self.user)
        response = self.client.post(reverse('api_v2:me_add_new_tag'), {"tag": new_tag})
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(1, len(CalendarTag.objects.filter(tag=new_tag)))

    def test_me_event_get(self):
        # test event
        test_events = [self.private_event, self.public_event]
        for event in test_events:
            with self.subTest():
                self.client = authenticated_client_factory(self.user)
                response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, event.slug]))
                response_data = convert_response(response.content)
                expect = json.dumps(CalendarEventSerializer(event).data)
                self.assertEqual(HTTP_200_OK, response.status_code)
                self.assertJSONEqual(expect, response_data)

    def test_me_event_get_with_unlogin(self):
        # test event
        test_events = [self.private_event, self.public_event]
        for event in test_events:
            with self.subTest():
                response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, event.slug]))
                self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_me_event_get_not_owned_event(self):
        """Test that api returns 403 when request for the other's event"""
        self.client = authenticated_client_factory(self.user)
        response = self.client.get(reverse('api_v2:me_event', args=[self.other_calendar.slug, self.other_event.slug]))
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)

    def test_me_event_put_with_not_owned_event(self):
        """Test that api returns 403 when request change for the other's event"""
        self.client = authenticated_client_factory(self.user)
        change_data = {
            "name": "new_name",
            "description": "new desc",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tag": self.public_tag.tag
        }
        response = self.client.put(
            reverse('api_v2:me_event', args=[self.other_calendar.slug, self.other_event.slug]),
            change_data
        )
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)
        self.assertNotEqual(change_data["name"], self.other_event.name)

    def test_me_event_put_change_event_name(self):
        # change private event to public event and change name
        self.client = authenticated_client_factory(self.user)
        change_data = {
            "name": "new name",
            "description": "new desc",
            "start_date": self.start_date + timedelta(days=1),
            "end_date": self.end_date + timedelta(days=1),
            "tag": self.public_tag.tag
        }
        response = self.client.put(
            reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]),
            change_data
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        # find change data
        response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, generate_slug(change_data["name"])]))
        response_data = convert_response(response.content)
        expect = json.dumps(CalendarEventSerializer(
            CalendarEvent.objects.get(name=change_data["name"])).data
        )
        self.assertJSONEqual(expect, response_data)
        # find previous event (should not found)
        response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]))
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_me_event_put_dont_change_event_name(self):
        # change private event to public event but don't change name
        self.client = authenticated_client_factory(self.user)
        change_data = {
            "name": self.private_event.name,
            "description": "new desc",
            "start_date": self.start_date + timedelta(days=1),
            "end_date": self.end_date + timedelta(days=1),
            "tag": self.public_tag.tag
        }
        response = self.client.put(
            reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]),
            change_data
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        # find change data, event data must not changed
        response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, generate_slug(change_data["name"])]))
        response_data = convert_response(response.content)
        expect = json.dumps(CalendarEventSerializer(
            CalendarEvent.objects.get(name=change_data["name"])).data
        )
        self.assertJSONEqual(expect, response_data)

    def test_me_event_put_exist_event_name(self):
        """Test that api returns 400 and does not change event detail when event name is already exist"""
        # change private event to public event but don't change name
        self.client = authenticated_client_factory(self.user)
        change_data = {
            "name": self.public_event.name,
            "description": "new desc",
            "start_date": self.start_date + timedelta(days=1),
            "end_date": self.end_date + timedelta(days=1),
            "tag": self.public_tag.tag
        }
        response = self.client.put(
            reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]),
            change_data
        )
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        # according to invalid data, event detail should not change
        response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]))
        response_data = convert_response(response.content)
        expect = json.dumps(CalendarEventSerializer(self.private_event).data)
        self.assertJSONEqual(expect, response_data)

    def test_me_event_put_with_not_available_tag(self):
        """Test that api returns 400 and does not change event detail whne event tag is not available"""
        # change detial using not owned tag
        self.client = authenticated_client_factory(self.user)
        change_data = {
            "name": self.private_event.name,
            "description": "new desc",
            "start_date": self.start_date + timedelta(days=1),
            "end_date": self.end_date + timedelta(days=1),
            "tag": self.other_tag.tag
        }
        response = self.client.put(
            reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]),
            change_data
        )
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        # according to invalid data, event detail should not change
        response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]))
        response_data = convert_response(response.content)
        expect = json.dumps(CalendarEventSerializer(self.private_event).data)
        self.assertJSONEqual(expect, response_data)

    def test_me_event_put_with_invalid_datetime(self):
        """Test that api returns 400 and does not change event detail then event datetime is invalid"""
        # change detial using invalid datetime
        self.client = authenticated_client_factory(self.user)
        change_data = {
            "name": self.private_event.name,
            "description": "new desc",
            "start_date": self.start_date + timedelta(days=1),
            "end_date": self.end_date,
            "tag": self.private_tag.tag
        }
        response = self.client.put(
            reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]),
            change_data
        )
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        # according to invalid data, event detail should not change
        response = self.client.get(reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]))
        response_data = convert_response(response.content)
        expect = json.dumps(CalendarEventSerializer(self.private_event).data)
        self.assertJSONEqual(expect, response_data)

    def test_me_event_delete(self):
        """Test that api completely delete event after sending delete request"""
        # try to delete private event
        self.client = authenticated_client_factory(self.user)
        response = self.client.delete(reverse('api_v2:me_event', args=[self.calendar.slug, self.private_event.slug]))
        self.assertEqual(HTTP_200_OK, response.status_code)
        # deleted event should not be exist
        with self.assertRaises(CalendarEvent.DoesNotExist):
            _ = CalendarEvent.objects.get(name=self.private_event.name)
