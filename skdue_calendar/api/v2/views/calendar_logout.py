from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# class Logout(APIView):

#     def get(self, request):
#         logout(request)
#         data = {"status": "logged out"}
#         return Response(data)

class Logout(APIView):
    # comment line below if you want to test only in back-end
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({"msg": "token expired"})