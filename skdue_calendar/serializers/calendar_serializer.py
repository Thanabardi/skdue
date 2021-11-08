from rest_framework import serializers
from skdue_calendar.models import Calendar


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url",
            "user"
        )