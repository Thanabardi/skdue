from copy import error
from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from skdue_calendar.serializers import *
from skdue_calendar.models import *
from skdue_calendar.utils import generate_slug


def get_available_tag(user, is_private=False):
    # default tags are available for all user
    defalut_tags = CalendarTag.objects.filter(tag_type__tag_type="default")
    # custom tags are available for creator
    my_tags = CalendarTag.objects.filter(user=user).filter(tag_type__tag_type="custom")
    # private tag is private tag
    if is_private:
        private_tag = CalendarTag.objects.filter(tag_type__tag_type="private")
        return chain(private_tag, defalut_tags, my_tags)
    return chain(defalut_tags, my_tags)

def get_custom_tag(user):
    tags = CalendarTag.objects.filter(user=user)
    custom_tag = tags.filter(tag_type__tag_type="custom")
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
                "available_tag": CalendarTagSerializer(get_available_tag(user, is_private=True), many=True).data
            }
            return Response(data)
        return Response({"msg": "login required"}, 403)


class UserMeCalendarView(APIView):
    def get(self, request, calendar_slug):
        """User calendar detail with public, private, and followed events"""
        if request.user.id == Calendar.objects.get(slug=calendar_slug).user.id:
            user = request.user
            # load follow status
            follow_status = FollowStatus.objects.filter(user=user)
            followed_user = [ u.followed for u in follow_status ]
            # load calendar
            calendar = Calendar.objects.get(slug=calendar_slug)
            # load my private event
            private_event = CalendarEvent.objects.filter(calendar=calendar)
            private_event = private_event.filter(tag__tag_type__tag_type="private")
            # set up data field
            data = {
                "user": UserSerializer(user).data,
                "calendar": CalendarSerializer(calendar).data,
                "event": {
                    "private": CalendarEventSerializer(private_event, many=True).data,
                }
            }
            # load my event
            data_event = data["event"]
            for tag in get_available_tag(user):
                events = CalendarEvent.objects.filter(calendar=calendar).filter(tag=tag)
                try:
                    data_event[tag.tag] += CalendarEventSerializer(events, many=True).data
                except:
                    data_event[tag.tag] = CalendarEventSerializer(events, many=True).data
            # load follwed people event
            calendar_load_user = followed_user
            for u in calendar_load_user:
                # admin has multiple calendar
                for c in Calendar.objects.filter(user=u):
                    for tag in get_available_tag(u):
                        print(u, c, tag)
                        events = CalendarEvent.objects.filter(calendar=c).filter(tag=tag)
                        try:
                            data_event[tag.tag] += CalendarEventSerializer(events, many=True).data
                        except:
                            data_event[tag.tag] = CalendarEventSerializer(events, many=True).data
            data["tag"] = data_event.keys()
            return Response(data)
        return Response({"msg": "login required"}, 403)
        

    def post(self, request, calendar_slug):
        """Create new calendar event
        
        Args:
            event_data: a dict consist of,
                - name: calendar event name
                - description: description of event
                - start_date: format (YYYY-MM-DD hh:mm:ss)
                - end_date: same format as start_date
                - tag: name of event tag
                - optional:
                    - is_test: True for testing, False otherwise

        Returns:
            dict: response data
        """
        if request.user.id == Calendar.objects.get(slug=calendar_slug).user.id:
            event_data = request.data
            if CalendarEvent.is_valid(event_data, calendar_slug) and CalendarEvent.is_usable_tag(event_data["tag"], user_id=request.user.id):
                calendar = Calendar.objects.get(slug=calendar_slug)
                slug = generate_slug(event_data["name"]) 
                tag = CalendarTag.objects.get(tag=event_data["tag"])
                new_event = CalendarEvent(
                    calendar = calendar,
                    name = event_data["name"],
                    slug = slug,
                    description = event_data["description"],
                    start_date = event_data["start_date"],
                    end_date = event_data["end_date"],
                    tag = tag
                )
                # When testing, this event will not included in database
                if "is_test" not in event_data.keys() or event_data["is_test"].lower() != "true":
                    new_event.save()
                new_event = CalendarEvent.objects.get(calendar__slug=calendar_slug, slug=slug)
                serializers = CalendarEventSerializer(new_event)
                data = serializers.data
                data["status"] = "success"
                data["msg"] = "calendar event created"
                # id of event will be null when `is_test` == true
                return Response(data, 201)
            else:
                return Response({"msg": "invalid event data"}, 400)
        return Response({"msg": "login required"}, 403) 


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
        follow_id = request.data["follow_id"]
        followed_user = User.objects.get(id=follow_id)
        if FollowStatus.is_valid(request.user, followed_user):
            fs = FollowStatus(user=request.user, followed=followed_user)
            fs.save()
            return Response({"msg": "followed"}, 201)
        return Response({"msg": "error"})


class UserMeAddTagView(APIView):
    def post(self, request):
        """User can add new custom tag from here"""
        if request.user.id:
            user = request.user
            if len(CalendarTag.objects.filter(tag=request.data["tag"])) == 0:
                new_custom_tag = CalendarTag(
                    user = user,
                    tag = request.data["tag"],
                    tag_type = CalendarTagType.objects.get(tag_type="custom")
                )
                new_custom_tag.save()
                return Response(CalendarTagSerializer(new_custom_tag).data)
            else:
                return Response({"msg": f"tag: {request.data['tag']} is already exist"}, 400)
        return Response({"msg": "login required"}, 403)
