import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import *
from skdue_calendar.models import FollowStatus, Calendar
from .utils import convert_response
from skdue_calendar.utils import generate_slug

def create_account(user, password):
    """To create Mockup user."""
    return User.objects.create_user(
                     username=user,
                     password=password,
                     email=f"{user}@mail.com")


class FollowStatusTests(TestCase):
    def setUp(self):
        # create user1
        self.user1 = create_account("patlom", "lompat-rankrank!")
        self.user1.first_name = "Patlom"
        self.user1_calendar = Calendar(
            user=self.user1,
            name=self.user1.username,
            slug=generate_slug(self.user1.username)
        )
        self.user1.save()
        self.user1_calendar.save()
        # create user2
        self.user2 = create_account("harry", "hackme22")
        self.user2.first_name = "Harry"
        self.user2_calendar = Calendar(
            user=self.user2,
            name=self.user2.username,
            slug=generate_slug(self.user2.username)
        )
        self.user2.save()
        self.user2_calendar.save()
        # create user3
        self.user3 = create_account("tester", "tester_pwd")
        self.user3.save()
        #follow

        FollowStatus.objects.create(user=self.user1, followed=self.user2, followed_calendar=self.user2_calendar)
    def test_get(self):
        """Response is the list of all follow_status in JSON form"""
        expect_data = []
        for fs in FollowStatus.objects.all():
            data = {
                "user": fs.user.id,
                "user_name": fs.user.username,
                "followed": fs.followed.id,
                "followed_name": fs.followed.username,
                "followed_calendar": fs.followed_calendar.id,
                "followed_calendar_slug": fs.followed_calendar.slug,
            }
            expect_data.append(data)
        expect_data = json.dumps(expect_data)
        response = self.client.get(reverse('api_v2:follow_status'))
        response_data = convert_response(response.content)
        self.assertJSONEqual(expect_data, response_data)

    def test_post(self):
        """Test that user can't create new user status from `api/v2/follow_status` end point"""
        response = self.client.post(reverse('api_v2:follow_status'))
        self.assertEqual(HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        print()
        print("tested")
