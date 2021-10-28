from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import Calendar
from skdue_calendar.serializers import CalendarSerializer
from skdue_calendar.utils import generate_slug


class CalendarList(APIView):
    """Request for list of calendar or create the new one."""

    def get(self, request, format=None):
        calendars = Calendar.objects.all()
        serializers = CalendarSerializer(calendars, many=True)
        return Response(serializers.data)

    def post(self, request):
        """Create new calendar
        
        Args:
            calendar_data: a dict consist of,
                - name: calendar name
                - optional:
                    - is_test: True for testing, False otherwise

        Returns:
            dict: response data
        """
        calendar_data = request.data
        if Calendar.is_valid(calendar_data):
            slug = generate_slug(calendar_data["name"])
            user = User.objects.get(id=calendar_data["user"])
            new_calendar = Calendar(
                name = calendar_data["name"],
                slug = slug,
                user = user
            )
            if  "is_test" not in calendar_data.keys() or calendar_data["is_test"].lower() != "true":
                new_calendar.save()
            serializers = CalendarSerializer(new_calendar)
            data = serializers.data
            data["status"] = "success" # add created status
            data["msg"] = "calendar created"
            return Response(data)
        return Response({"status": "failed", "msg": "invalid calendar"})