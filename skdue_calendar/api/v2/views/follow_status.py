from rest_framework.views import APIView
from rest_framework.response import Response

from skdue_calendar.models import FollowStatus
from skdue_calendar.serializers import FollowStatusSerializer


class FollowStatusView(APIView):

    def get(self, request, format=None):
        fs = FollowStatus.objects.all()
        serializers = FollowStatusSerializer(fs, many=True)
        return Response(serializers.data)

    def post(self, request):
        fs_data = request.data

        print(fs_data)
        if FollowStatus.is_valid(fs_data["user"], fs_data["followed"]):
            fs = FollowStatus(
                user = fs_data["user"],
                follower = fs_data["followed"],
            )
            #   hacve no clue about this stuff
            # if  "is_test" not in calendar_data.keys() or calendar_data["is_test"].lower() != "true":
            #     new_calendar.save()
            fs.save()
            serializers = FollowStatusSerializer(fs)
            data = serializers.data
            data["status"] = "success" # add created status
            data["msg"] = "follower_status created"
            return Response(data)
        return Response({"status": "failed", "msg": "invalid calendar"})
