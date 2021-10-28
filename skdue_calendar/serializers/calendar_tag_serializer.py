from rest_framework import serializers
from skdue_calendar.models import CalendarTag


class CalendarTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarTag
        fields = (
            "id",
            "tag"
        )