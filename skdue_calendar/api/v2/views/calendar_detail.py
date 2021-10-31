from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from itertools import chain

from django.contrib.auth.models import User
from skdue_calendar.models import *
from skdue_calendar.serializers import *


class CalendarDetailView(APIView):
    """Request for list of events in an calendar or create new events in that calendar."""
    def get_tagged_event(self, calendar_slug, tag):
        try:
            calendar = Calendar.objects.get(slug=calendar_slug)
            return CalendarEvent.objects.filter(calendar=calendar).filter(tag=tag)
        except (Calendar.DoesNotExist, CalendarEvent.DoesNotExist):
            raise Http404

    def get_public_tag(self, user):
        default_tag = CalendarTag.objects.filter(tag_type__tag_type="default")
        custom_tag = CalendarTag.objects.filter(user=user).filter(tag_type__tag_type="custom")
        return chain(default_tag, custom_tag)

    def get(self, request, calendar_slug, format=None):
        calendar = Calendar.objects.get(slug=calendar_slug)
        user = User.objects.get(id=calendar.user.id)
        tag = self.get_public_tag(user)
        data = {
            "user": UserSerializer(user).data,
            "calendar": CalendarSerializer(calendar).data,
            "event": {},
        }
        for t in tag:
            tagged_event = self.get_tagged_event(calendar_slug, t)
            data["event"][t.tag] = CalendarEventSerializer(tagged_event, many=True).data
        data["tag"] = data["event"].keys()
        return Response(data)
