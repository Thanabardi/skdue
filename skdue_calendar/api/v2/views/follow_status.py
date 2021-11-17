from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *

from skdue_calendar.models import FollowStatus
from skdue_calendar.serializers import FollowStatusSerializer


class FollowStatusView(APIView):
    """Request for list of follow_status or add the new one."""

    def get(self, request, format=None):
        fs = FollowStatus.objects.all()
        serializers = FollowStatusSerializer(fs, many=True)
        return Response(serializers.data)
