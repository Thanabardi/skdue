from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import CalendarEvent
from skdue_calendar.serializers import CalendarEventSerializer


class EventDetail(APIView):
    """Request for detail of specific event in an specific calendar."""

    def get_object(self, calendar_slug, event_slug=None):
        try:
            if(event_slug):
                return CalendarEvent.objects.filter(calendar__slug=calendar_slug).get(slug=event_slug)
        except CalendarEvent.DoesNotExist:
            raise Http404

    def get(self, request, calendar_slug, event_slug, format=None):
        events = self.get_object(calendar_slug, event_slug)
        serializers = CalendarEventSerializer(events)
        return Response(serializers.data)