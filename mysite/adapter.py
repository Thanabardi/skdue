from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from skdue_calendar.models import Calendar
from skdue_calendar.utils import generate_slug
from django.contrib.auth.models import User
from mysite.settings import CORS_ALLOWED_ORIGINS
from rest_framework.response import Response
from django.urls import reverse

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        print(request)
        new_user = request.user
        user_calendar, created = Calendar.objects.get_or_create(
            user = User.objects.get(username=new_user.username),
            defaults={
                "name": new_user.username,
                "slug": generate_slug(new_user.username)})

        # path = "{fornt_end_path}/me/{username}/"

        # return path.format(fornt_end_path=CORS_ALLOWED_ORIGINS[0], username=new_user.username)

        return reverse("api_v2:get_auth_token")
