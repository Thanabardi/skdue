from rest_framework.views import APIView
from rest_framework.response import Response
from skdue_calendar.serializers import UserSettingSerializer
from skdue_calendar.models import UserSetting

class UserSettingView(APIView):
    def get(self, request):
        data = UserSettingSerializer(UserSetting.objects.all(), many=True).data
        return Response(data)

    def post(self, request):
        file = request.data['file']
        image = UserSetting.objects.create(image=file)
        return Response({'message': "Uploaded"})

    def put(self, request):
        pass