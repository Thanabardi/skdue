from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import FollowStatus
from skdue_calendar.serializers import FollowStatusSerializer


class FollowStatusView(APIView):
    """Request for list of follow_status or add the new one."""

    def get(self, request, format=None):
        fs = FollowStatus.objects.all()
        serializers = FollowStatusSerializer(fs, many=True)
        return Response(serializers.data)

    def post(self, request):
        """Create new follow_status

        Args:
            fs_data: a dict consist of,
                - user: user model
                - followed: user model

        Returns:
            dict: response data
        """
        fs_data = request.data
        if FollowStatus.is_valid(fs_data["user"], fs_data["followed"]):
            fs = FollowStatus(
                user = fs_data["user"],
                follower = fs_data["followed"],
            )
            fs.save()
            serializers = FollowStatusSerializer(fs)
            data = serializers.data
            data["status"] = "success" # add created status
            data["msg"] = "follower_status created"
            return Response(data)
        return Response({"status": "failed", "msg": "invalid calendar"})
