from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from skdue_calendar.models import Calendar
from skdue_calendar.utils import generate_slug
from skdue_calendar.serializers import CalendarSerializer

from django.views.decorators.csrf import csrf_exempt


class Register(APIView):

    def is_valid(self, request):
        username = request.data["username"]
        try:
            _ = User.objects.get(username=username)
        except User.DoesNotExist:
            return True
        return False
       
    @csrf_exempt
    def post(self, request):
        user = request.data
        if self.is_valid(request):
            # create new user
            new_user = User.objects.create_user(user['username'], user['email'], user['password'])
            new_user.save()
            # Create new calendar
            name = user["username"]
            slug = generate_slug(name)
            new_calendar = Calendar(
                name = name,
                slug = slug,
                user = new_user
            )
            new_calendar.save()
            serializers = CalendarSerializer(new_calendar)
            data = serializers.data
            data["status"] = "success" # add created status
            data["msg"] = "Account created"
            return Response(data)
        else:
            return Response({"status": "failed", "msg": "Account created fail"})
        