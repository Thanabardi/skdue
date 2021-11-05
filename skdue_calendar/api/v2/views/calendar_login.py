from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from skdue_calendar.models import Calendar
from skdue_calendar.serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login

from skdue_calendar.serializers.calendar_serializer import CalendarSerializer

class Login(APIView):

    @csrf_exempt
    def post(self, request):
        
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            data = {
                "user":UserSerializer(user).data,
                "calendar":CalendarSerializer(Calendar.objects.get(user=user)).data
            }
            login(request, user)
            return Response(data)
        else:
            raise Http404
