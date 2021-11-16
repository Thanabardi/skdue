from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class Logout(APIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,) 

    # def get(self, request):
    #     logout(request)
    #     data = {"status": "logged out"}
    #     return Response(data)

    def delete(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"msg": "token expired"})