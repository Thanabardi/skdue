import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import FollowStatus
from .utils import convert_response

def create_account(user, password):
    """To create Mockup user."""
    return User.objects.create_user(
                     username=user,
                     password=password,
                     email=f"{user}@mail.com")


class CalendarListTests(TestCase):
    def setUp(self):
        # create user1
        self.user1 = create_account("patlom", "lompat-rankrank!")
        self.user1.first_name = "Patlom"
        self.user1.save()
        # create user2
        self.user2 = create_account("harry", "hackme22")
        self.user2.first_name = "Harry"
        self.user2.save()
        #follow
        FollowStatus.objects.create(user=self.user1, followed=self.user2)

    def test_get(self):
        """Response is the list of all follow_status in JSON form"""
        expect_data = []
        for fs in FollowStatus.objects.all():
            data = {
                "user": fs.user.id,
                "user_name": fs.user.username,
                "followed": fs.followed.id,
                "followed_name": fs.followed.username,
            }
            expect_data.append(data)
        expect_data = json.dumps(expect_data)
        response = self.client.get(reverse('api_v2:fs'))
        response_data = convert_response(response.content)
        self.assertJSONEqual(expect_data, response_data)

    def test_post_with_invalid_follow_status_data(self):
        """Response is the fail status with message"""
        # TODO: add this test case after implement new `is_valid` method in `FollowStatus` model
        # what to test status_code, resounse_data
        pass

    def test_post_with_valid_follow_status_data(self):
        """Response is the new follow status data with success status"""
        # TODO: add this test case after implement new `is_valid` method in `FollowStatus` model
        # what to test status_code, resounse_data
        pass
