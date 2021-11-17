from django.test import TestCase
from skdue_calendar.models import FollowStatus, Calendar
from django.contrib.auth.models import User
from skdue_calendar.utils import generate_slug

def create_account(user, password):
    """To create Mockup user."""
    return User.objects.create_user(
                     username=user,
                     password=password,
                     email=f"{user}@mail.com")

class FollowStatusModelTest(TestCase):

    def setUp(self):
        super().setUp()
        # create user1
        self.user1 = create_account("patlom", "lompat-rankrank!")
        self.user1.first_name = "Patlom"
        self.calendar1 = Calendar(
            user=self.user1,
            name=self.user1.username,
            slug=generate_slug(self.user1.username)
        )
        self.user1.save()
        self.calendar1.save()
        # create user2
        self.user2 = create_account("harry", "hackme22")
        self.user2.first_name = "Harry"
        self.calendar2 = Calendar(
            user=self.user2,
            name=self.user2.username,
            slug=generate_slug(self.user2.username)
        )
        self.user2.save()
        self.calendar2.save()
        # create user3
        self.user3 = create_account("johny", "hackme22")
        self.user3.first_name = "John"
        self.calendar3 = Calendar(
            user=self.user3,
            name=self.user3.username,
            slug=generate_slug(self.user3.username)
        )
        self.user3.save()
        self.calendar3.save()

    def test_follow(self):
        """Test user follow and string."""
        follow = FollowStatus.objects.create(user=self.user1, followed=self.user2, followed_calendar=self.calendar2)
        self.assertEqual(f'{self.user1.username} has FOLLOWED {self.user2.username}', str(follow))

    def test_multiple_following(self):
        """User should not follow same account twices."""
        follow = FollowStatus.objects.create(user=self.user1, followed=self.user2, followed_calendar=self.calendar2)
        self.assertFalse(FollowStatus.is_valid(self.user1, self.user2, self.calendar2))

    def test_is_valid(self):
        """User should not follow user account itself."""
        self.assertFalse(FollowStatus.is_valid(self.user1, self.user1, self.calendar1))
        self.assertFalse(FollowStatus.is_valid(self.user2, self.user2, self.calendar2))

    def test_unfollow(self):
        """Test unfollow method."""
        follow = FollowStatus.objects.create(user=self.user1, followed=self.user2, followed_calendar=self.calendar2)
        # follow.unfollow()
        FollowStatus.objects.filter(user=self.user1, followed=self.user2)[0].unfollow()
        self.assertTrue(FollowStatus.is_valid(self.user1, self.user2, self.calendar2))
        #follow again
        follow = FollowStatus.objects.create(user=self.user1, followed=self.user2, followed_calendar=self.calendar2)
        self.assertFalse(FollowStatus.is_valid(self.user1, self.user2, self.calendar2))

    def test_followed_list(self):
        """Show list of people who user1 has been followed."""
        FollowStatus.objects.create(user=self.user1, followed=self.user2, followed_calendar=self.calendar2)
        FollowStatus.objects.create(user=self.user1, followed=self.user3, followed_calendar=self.calendar3)

        self.assertEqual(2, len(FollowStatus.objects.filter(user=self.user1)))

        list_followed =[]
        for f in FollowStatus.objects.filter(user=self.user1):
            list_followed.append(f.followed)
        self.assertEqual(list_followed, [self.user2, self.user3])
