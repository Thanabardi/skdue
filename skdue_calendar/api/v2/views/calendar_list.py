from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import Calendar
from skdue_calendar.serializers import CalendarSerializer
from skdue_calendar.utils import generate_slug


class CalendarListView(APIView):
    """Request for list of calendar or create the new one."""

    def get(self, request, format=None):
        calendars = Calendar.objects.all()
        serializers = CalendarSerializer(calendars, many=True)
        return Response(serializers.data)
