from rest_framework import serializers
from skdue_calendar.models import CalendarEvent


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url",
            "description",
            "start_date",
            "end_date"
        )
