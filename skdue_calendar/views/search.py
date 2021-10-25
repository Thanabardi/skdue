from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import Calendar, CalendarEvent
from skdue_calendar.serializers import CalendarSerializer, CalendarEventSerializer


class Search(APIView):
    """Request for not private detail."""

    def get(self, request):
        calendar = Calendar.objects.all()
        calendar_serializer = CalendarSerializer(calendar, many=True)
        events = CalendarEvent.objects.all()
        events_serializer = CalendarEventSerializer(events, many=True)
        data = {
            "calendar": calendar_serializer.data,
            "event": events_serializer.data
        } 
        return Response(data)