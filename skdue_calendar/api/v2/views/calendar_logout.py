from django.contrib.auth import logout
from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

class Logout(APIView):

    def get(self, request):
        logout(request)
        data = {"status": "logged out"}
        return Response(data)