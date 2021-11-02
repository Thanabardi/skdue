from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from skdue_calendar.serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login

class Login(APIView):

    @csrf_exempt
    def post(self, request):
        
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            raise Http404
