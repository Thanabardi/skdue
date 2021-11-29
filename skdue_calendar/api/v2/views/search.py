from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from skdue_calendar.models import *
from skdue_calendar.serializers import CalendarSerializer, CalendarEventSerializer, CalendarTagSerializer


class SearchView(APIView):
    """Request for not private detail."""

    def get(self, request):
        calendars = Calendar.objects.all()
        calendar_serializer = CalendarSerializer(calendars, many=True)
        events = CalendarEvent.objects.exclude(tag__tag="private")
        events_serializer = CalendarEventSerializer(events, many=True)
        tags = CalendarTag.objects.exclude(tag="private")
        tags_serializer = CalendarTagSerializer(tags, many=True)
        data = {
            "calendar": calendar_serializer.data,
            "event": events_serializer.data,
            "tag": tags_serializer.data
        } 
        return Response(data)
