from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import Calendar, CalendarEvent, CalendarTag
from skdue_calendar.serializers import CalendarSerializer, CalendarEventSerializer, CalendarTagSerializer


class Search(APIView):
    """Request for not private detail."""

    def get(self, request):
        calendars = Calendar.objects.all()
        calendar_serializer = CalendarSerializer(calendars, many=True)
        events = CalendarEvent.objects.all()
        events_serializer = CalendarEventSerializer(events, many=True)
        tags = CalendarTag.objects.all()
        tags_serializer = CalendarTagSerializer(tags, many=True)
        data = {
            "calendar": calendar_serializer.data,
            "event": events_serializer.data,
            "tag": tags_serializer.data
        } 
        return Response(data)