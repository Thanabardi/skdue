from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import Calendar, CalendarEvent
from skdue_calendar.models.calendar_tag import CalendarTag
from skdue_calendar.serializers import CalendarEventSerializer
from skdue_calendar.utils import generate_slug


class CalendarEventList(APIView):
    """Request for list of events in an calendar or create new events in that calendar."""
    def get_object(self, calendar_slug):
        try:
            calendar = Calendar.objects.get(slug=calendar_slug)
            return CalendarEvent.objects.filter(calendar=calendar)
        except (Calendar.DoesNotExist, CalendarEvent.DoesNotExist):
            raise Http404

    def get(self, request, calendar_slug, format=None):
        events = self.get_object(calendar_slug)
        serializers = CalendarEventSerializer(events, many=True)
        return Response(serializers.data)

    def post(self, request, calendar_slug, format=None):
        """Create new calendar
        
        Args:
            event_data: a dict consist of,
                - name: calendar event name
                - description: description of event
                - start_date: format (YYYY-MM-DD hh:mm:ss)
                - end_date: same format as start_date
                - optional:
                    - is_test: True for testing, False otherwise

        Returns:
            dict: response data
        """
        event_data = request.data
        if CalendarEvent.is_valid(event_data, calendar_slug):
            calendar = Calendar.objects.get(slug=calendar_slug)
            slug = generate_slug(event_data["name"]) 
            tag = CalendarTag.objects.get(tag=event_data["tag"])
            new_event = CalendarEvent(
                calendar = calendar,
                name = event_data["name"],
                slug = slug,
                description = event_data["description"],
                start_date = event_data["start_date"],
                end_date = event_data["end_date"],
                tag = tag
            )
            # When testing, this event will not included in database
            if "is_test" not in event_data.keys() or event_data["is_test"].lower() != "true":
                new_event.save()
            new_event = CalendarEvent.objects.get(calendar__slug=calendar_slug, slug=slug)
            serializers = CalendarEventSerializer(new_event)
            data = serializers.data
            data["status"] = "success"
            data["msg"] = "calendar event created"
            # id of event will be null when `is_test` == true
            return Response(data)
        return Response({"status": "failed", "msg": "invalid calendar event"})