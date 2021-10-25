from rest_framework import serializers
from .models import Calendar, CalendarEvent


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


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url"
        )