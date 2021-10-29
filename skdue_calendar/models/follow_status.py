from django.db import models
from django.contrib.auth.models import User

class FollowStatus(models.Model):
    """ USER are follow the FOLLOWED user """

    user = models.ForeignKey(
            User,
            null=False,
            blank=False,
            on_delete=models.CASCADE,
            related_name='user')
    followed = models.ForeignKey(
            User,
            null=False,
            blank=False,
            on_delete=models.CASCADE,
            related_name='followed')

    @property
    def user_name(self):
        return self.user.username
    @property
    def followed_name(self):
        return self.followed.username

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f'{self.user.username} has FOLLOWED {self.followed.username}'

    def unfollow(self):
        self.delete()
        print(f'{self.user.username} has UNFOLLOWED {self.followed.username}')

    @classmethod
    def is_valid(self, user, follower):
        # print(FollowStatus.objects.filter(user=user, follower=follower))
        if user == followed:
            return False
        if len(FollowStatus.objects.filter(user=user, followed=followed)) != 0:
            return False
        return True
