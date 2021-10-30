from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.serializers import *
from skdue_calendar.models import *

try:
    DEFAULT_TAG_TYPE = CalendarTagType.objects.get(tag_type="default")
except CalendarTagType.DoesNotExist:
    tag = CalendarTagType(tag_type="default")
    tag.save()
    DEFAULT_TAG_TYPE = CalendarTagType.objects.get(tag_type="default")

try:
    PRIVATE_TAG_TYPE = CalendarTagType.objects.get(tag_type="private")
except CalendarTagType.DoesNotExist:
    tag = CalendarTagType(tag_type="private")
    tag.save()
    PRIVATE_TAG_TYPE = CalendarTagType.objects.get(tag_type="private")

try:
    CUSTOM_TAG_TYPE = CalendarTagType.objects.get(tag_type="custom")
except CalendarTagType.DoesNotExist:
    tag = CalendarTagType(tag_type="custom")
    tag.save()
    CUSTOM_TAG_TYPE = CalendarTagType.objects.get(tag_type="custom")


def get_available_tag(user):
    # default tags are available for all user
    defalut_tags = CalendarTag.objects.filter(tag_type=DEFAULT_TAG_TYPE)
    # custom tags are available for creator
    my_tags = CalendarTag.objects.filter(user=user).filter(tag_type=CUSTOM_TAG_TYPE)
    # private tag is private tag
    private_tag = CalendarTag.objects.filter(tag_type=PRIVATE_TAG_TYPE)
    return chain(private_tag, defalut_tags, my_tags)

def get_custom_tag(user):
    tags = CalendarTag.objects.filter(user=user)
    custom_tag = tags.filter(tag_type=CUSTOM_TAG_TYPE)
    return custom_tag


class UserMeView(APIView):
    def get(self, request):
        if request.user.id:
            user = request.user
            calendar = Calendar.objects.filter(user=user)
            data = {
                "user": UserSerializer(user).data,
                "calendar": CalendarSerializer(calendar, many=True).data,
                "my_custom_tag": CalendarTagSerializer(get_custom_tag(user), many=True).data,
                "available_tag": CalendarTagSerializer(get_available_tag(user), many=True).data
            }
            return Response(data)
        return Response({"msg": "login required"}, 403)


class UserMeCalendarView(APIView):
    def get(self, request, calendar_slug):
        """User calendar detail with public and private events"""
        if request.user.id:
            # load follow status
            # load my event
            # load follwed people event
            pass
        return Response({"msg": "login required"}, 403)
        

    def post(self, request, calendar_slug):
        """User can create new event from here"""
        pass


class UserMeFollowedView(APIView):
    def get(self, request):
        """Get list of user's follwed people"""
        if request.user.id:
            user = request.user
            follow_status = FollowStatus.objects.filter(user=user)
            return Response(FollowStatusSerializer(follow_status, many=True).data)
        return Response({"msg": "login required"}, 403)

    def post(self, request):
        """User can follow another user here"""
        pass

class UserMeAddTagView(APIView):
    def post(self, request):
        """User can add new custom tag from here"""
        if request.user.id:
            user = request.user
            new_custom_tag = CalendarTag(
                user = user,
                tag = request.data["tag"],
                tag_type = CUSTOM_TAG_TYPE
            )
            new_custom_tag.save()
            return Response(CalendarTagSerializer(new_custom_tag).data)
        return Response({"msg": "login required"}, 403)
