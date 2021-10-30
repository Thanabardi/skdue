from django.contrib.auth.models import User
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.serializers import UserSerializer
from skdue_calendar.models import *
from skdue_calendar.serializers.calendar_serializer import CalendarSerializer


class UserMeView(APIView):
    def get(self, request):
        if request.user.id:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        return Response({"msg": "login required"}, 403)


class UserMeCalendarView(APIView):
    def get(self, request):
        """User calendar detail with public and private events"""
        pass

    def post(self, request):
        """User can create new event from here"""
        pass


class UserMeFollowedView(APIView):
    def get(self, request):
        """Get list of user's follwed people"""
        pass