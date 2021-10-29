from django.contrib.auth import logout
from django.http.response import Http404
from rest_framework.views import APIView
from skdue_calendar import serializers
from skdue_calendar.serializers import LogoutSerializer
from rest_framework.response import Response

class Logout(APIView):

    def get(self, request):
        user = request.data
        logout(request)
        data = {"status": "logged out"}
        return Response(data)