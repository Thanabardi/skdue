from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from skdue_calendar.serializers import UserSerializer


class UserListView(APIView):
    """API for `/api/v2/users`"""
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
