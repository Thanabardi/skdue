from itertools import chain
from datetime import datetime
from django.urls import reverse
from django.shortcuts import redirect
from django.http.response import Http404, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

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
    """View of user's information"""

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

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
        return Response({"msg": "login required"}, HTTP_401_UNAUTHORIZED)


class UserMeCalendarView(APIView):
    """View of user's specific calendar information"""

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, calendar_slug):
        """User calendar detail with public, private, and followed events"""

        try:
            calendar = Calendar.objects.get(slug=calendar_slug)
        except Calendar.DoesNotExist:
            raise Http404

        if request.user.id == calendar.user.id:
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
        return Response({"msg": "login required or you are not calendar owner"}, HTTP_403_FORBIDDEN)


    def post(self, request, calendar_slug):
        """Create new calendar event

        Args:
            requset.data: a dict consist of,
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
                return Response(data, HTTP_201_CREATED)
            else:
                return Response({"msg": "invalid event data"}, HTTP_400_BAD_REQUEST)
        return Response({"msg": "login required"}, HTTP_401_UNAUTHORIZED)


class UserMeFollowedView(APIView):
    """View for user's follow status with follow/unfollow option"""

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get list of user's follwed people"""
        if request.user.id:
            user = request.user
            follow_status = FollowStatus.objects.filter(user=user)
            return Response(FollowStatusSerializer(follow_status, many=True).data)
        return Response({"msg": "login required"}, HTTP_401_UNAUTHORIZED)

    def post(self, request):
        """User can follow another user here"""
        opt = request.data["option"]
        follow_id = request.data["follow_id"]
        followed_user = User.objects.get(id=follow_id)
        follow_cal = request.data["follow_calendar"]
        followed_cal = Calendar.objects.get(id=follow_cal)
        if opt == "follow":
            if FollowStatus.is_valid(request.user, followed_user, followed_cal):
                # fs = FollowStatus(user=request.user, followed=followed_user)
                fs = FollowStatus(user=request.user, followed=followed_user, followed_calendar=followed_cal)
                fs.save()
                return Response({"msg": "followed"}, HTTP_201_CREATED)
            else:
                return Response({"msg": "invalid follow status"}, HTTP_400_BAD_REQUEST)
        elif opt == "unfollow":
            fs = FollowStatus.objects.get(user=request.user, followed=followed_user, followed_calendar=followed_cal)
            fs.unfollow()
            return Response({"msg": "unfollowed"}, HTTP_200_OK)
        return Response({"msg": "option not found"}, HTTP_404_NOT_FOUND)


class UserMeAddTagView(APIView):
    """View for adding new custom tag"""

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """User can add new custom tag from here"""
        if request.user.id:
            user = request.user
            if CalendarTag.is_valid(request.data):
                new_custom_tag = CalendarTag(
                    user = user,
                    tag = request.data["tag"],
                    tag_type = CalendarTagType.objects.get(tag_type="custom")
                )
                new_custom_tag.save()
                return Response(CalendarTagSerializer(new_custom_tag).data, HTTP_201_CREATED)
            else:
                return Response({"msg": f"tag: {request.data['tag']} is already exist"}, HTTP_400_BAD_REQUEST)
        return Response({"msg": "login required"}, HTTP_401_UNAUTHORIZED)

    def put(self, request):
        """Change tag text

        Args:
            requset.data: a dict consist of,
                - old_name: old text name before.
                - new_name: new name tag you want.

        """
        if request.user.id:
            try:
                changed_tag = CalendarTag.objects.get(user=request.user, tag=request.data["old_name"])
            except CalendarTag.DoesNotExist:
                raise Http404
            try:
                check_tag = CalendarTag.objects.get(user=request.user, tag=request.data["new_name"])
                return Response({"msg": "name tag was already in used"}, HTTP_400_BAD_REQUEST)
            except CalendarTag.DoesNotExist:
                print(changed_tag.tag)
                changed_tag.tag = request.data["new_name"]
                changed_tag.save()
                return Response({"msg": "tag edited"}, HTTP_200_OK)


    def delete(self, request):
        if request.user.id:
            user = request.user
            try:
                tag = request.GET.get('tag')
                print(tag)
                changed_tag = CalendarTag.objects.get(user=user,tag=tag)
                changed_tag.delete()
                return Response({"msg": "tag deleted"}, HTTP_200_OK)
            except:
                return Response({"msg": "given tag is invalid"}, HTTP_400_BAD_REQUEST)


class UserMeEventView(APIView):
    """View for user's calendar event with ability to editing event's detail"""

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def is_owner(self, user, calendar_slug) -> bool:
        try:
            calendar = Calendar.objects.get(slug=calendar_slug)
            return user.id == calendar.user.id
        except Calendar.DoesNotExist:
            raise Http404

    def get_event(self, calendar_slug, event_slug) -> CalendarEvent:
        try:
            event = CalendarEvent.objects.get(calendar__slug=calendar_slug, slug=event_slug)
            return event
        except CalendarEvent.DoesNotExist:
            raise Http404

    def get(self, request, calendar_slug, event_slug):
        if self.is_owner(request.user, calendar_slug):
            event = self.get_event(calendar_slug, event_slug)
            serializer = CalendarEventSerializer(event)
            return Response(serializer.data, HTTP_200_OK)
        return Response({"msg": "you are not the owner of this calendar"}, HTTP_403_FORBIDDEN)

    def put(self, request, calendar_slug, event_slug):
        """Change calendar event

        Args:
            requset.data: a dict consist of,
                - name: calendar event name
                - description: description of event
                - start_date: format (YYYY-MM-DD hh:mm:ss)
                - end_date: same format as start_date
                - tag: name of event tag
                - optional:
                    - is_test: True for testing, False otherwise

        Returns:
            dict: response data consist of,
                - msg
                - new_url (when event detail is successfully changed)
        """
        if self.is_owner(request.user, calendar_slug):
            event = self.get_event(calendar_slug, event_slug)

            # check tag availability
            try:
                changed_tag = CalendarTag.objects.get(tag=request.data["tag"])
            except CalendarTag.DoesNotExist:
                print('it tag!!!')
                raise Http404
            if changed_tag.id in [t.id for t in get_available_tag(request.user, is_private=True)]:
                event.tag = changed_tag
            else:
                return Response({"msg": "invalid tag"}, HTTP_400_BAD_REQUEST)

            # check name availability
            if event.name != request.data["name"]:
                try:
                    check_event = CalendarEvent.objects.get(
                        calendar__slug=calendar_slug,
                        name=request.data["name"]
                        )
                    print(check_event)
                    return Response({"msg": "the event name that you want to change is already exist in your calendar event"}, HTTP_400_BAD_REQUEST)
                except CalendarEvent.DoesNotExist:
                    event.name = request.data["name"]

            # check start and end date
            start_date = datetime.strptime(request.data["start_date"], "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(request.data["end_date"], "%Y-%m-%d %H:%M:%S")
            if start_date < end_date:
                event.start_date = request.data["start_date"]
                event.end_date = request.data["end_date"]
            else:
                return Response({"msg": "invalid datetime"}, HTTP_400_BAD_REQUEST)

            new_slug = generate_slug(request.data["name"])
            event.slug = new_slug
            event.description = request.data["description"]

            event.save()

            return Response(
                    {
                        "msg": "changed event detail",
                        "new_url": reverse('api_v2:me_event', args=[calendar_slug, new_slug])
                    },
                    HTTP_200_OK
                )
        else:
            return Response({"msg": "you are not the owner of this calendar"}, HTTP_403_FORBIDDEN)

    def delete(self, request, calendar_slug, event_slug):
        """Delete requested event"""
        if self.is_owner(request.user, calendar_slug):
            event = self.get_event(calendar_slug, event_slug)
            print(event)
            event.delete()
            return Response({"msg": "event deleted"}, HTTP_200_OK)
        else:
            return Response({"msg": "you are not the owner of this calendar"}, HTTP_403_FORBIDDEN)
