from rest_framework import serializers
from skdue_calendar.models import FollowStatus


class FollowStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowStatus
        fields = (
            "user",
            "user_name",
            "followed",
            "followed_name",
            "followed_calendar",
            "followed_calendar_slug"
        )
