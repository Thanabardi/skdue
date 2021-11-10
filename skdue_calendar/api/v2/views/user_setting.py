import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from skdue_calendar.serializers import UserSettingSerializer
from skdue_calendar.models import *

DEFAULT_IMAGE = "/images/default.jpg"


class UserSettingView(APIView):
    """user setting for public view"""

    def get(self, request, calendar_slug):
        try:
            calendar = Calendar.objects.get(slug=calendar_slug)
        except:
            return Response({"msg": "calendar not found"}, HTTP_404_NOT_FOUND)
        user = calendar.user
        user_setting, created = UserSetting.objects.get_or_create(
            user=calendar.user,
            defaults={
                "display_name": user.username,
                "image": DEFAULT_IMAGE})
        print("CREATED", created)
        return Response(UserSettingSerializer(user_setting).data)

class UserMeSetting(APIView):
    """view class that require authentication"""
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        user_setting, created = UserSetting.objects.get_or_create(
            user=request.user,
            defaults={
                "display_name": request.user.username,
                "image": DEFAULT_IMAGE
            }
        )
        return Response(UserSettingSerializer(user_setting).data)

    def put(self, request):
        user_setting = UserSetting.objects.get(user=request.user)
        old_img_url = user_setting.image.url
        try:
            user_setting.image = request.data["file"]
            user_setting.save()

            # remove old image, save space
            if DEFAULT_IMAGE != old_img_url:
                pass
            
        except:
            return Response({"msg": "invalid data"}, HTTP_400_BAD_REQUEST)
        return Response(UserSettingSerializer(user_setting).data, HTTP_202_ACCEPTED)
