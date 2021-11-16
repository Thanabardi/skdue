import os
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from skdue_calendar.serializers import *
from skdue_calendar.models import *

DEFAULT_IMAGE = "/images/default.jpg"
DEFAULT_THEME_TYPE = "light"
DEFAULT_THEME_NAME = "theme-1"
DEFAULT_TAG_COLOR = "white"


class UserSettingView(APIView):
    """User setting for public view"""

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
                "image": DEFAULT_IMAGE,
                "theme_type": DEFAULT_THEME_TYPE,
                "theme_name": DEFAULT_THEME_NAME
            })
        tags = CalendarTag.objects.filter(user=user)
        colors = {}
        for t in tags:
            # replace null value with default color
            if t.tag_color == None:
                t.tag_color = DEFAULT_TAG_COLOR
                t.save()
            colors[t.tag] = t.tag_color
        print(tags)
        data = {
            "setting": UserSettingSerializer(user_setting).data,
            "custom_tag": CalendarTagSerializer(tags, many=True).data,
            "color": colors,
        }
        return Response(data)


class UserMeSetting(APIView):
    """view class that require authentication"""

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        user_setting, created = UserSetting.objects.get_or_create(
            user=request.user,
            defaults={
                "display_name": request.user.username,
                "image": DEFAULT_IMAGE,
                "theme_type": DEFAULT_THEME_TYPE,
                "theme_name": DEFAULT_THEME_NAME
            }
        )
        tags = CalendarTag.objects.filter(user=request.user)
        colors = {}
        for t in tags:
            # replace null value with default color
            if t.tag_color == None:
                t.tag_color = DEFAULT_TAG_COLOR
                t.save()
            colors[t.tag] = t.tag_color
        data = {
            "setting": UserSettingSerializer(user_setting).data,
            "custom_tag": CalendarTagSerializer(tags, many=True).data,
            "color": colors,
        }
        return Response(data)

    def put(self, request):
        """Change setting data in form of http form below
        
        Args:
            request_data: a dict (in form of json) consint of,
                - file: image file of profile picture
                - display_name: str
                - about: str
                - color: a dict (in json) of color which key is tag name, 
                         value is color you want to change
        """
        user_setting = UserSetting.objects.get(user=request.user)
        old_img = user_setting.image
        # user setting
        try:
            # set data
            user_setting.image = request.data["file"]
            user_setting.display_name = request.data["display_name"]
            user_setting.about = request.data["about"]

            colors = json.loads(request.data["color"])
            tags = []
            for k in colors:
                tag = CalendarTag.objects.get(user=request.user, tag=k)
                tag.tag_color = colors[k]
                tags.append(tag)

            # save
            user_setting.save()
            for t in tags:
                t.save()

            # remove old image, save space
            if "/media"+DEFAULT_IMAGE != old_img.url:
                os.remove(old_img.path)
        except:
            return Response({"msg": "invalid data"}, HTTP_400_BAD_REQUEST)
        return Response({"msg": "setting updated"}, HTTP_202_ACCEPTED)
