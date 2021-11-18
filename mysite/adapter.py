from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from skdue_calendar.models import Calendar
from skdue_calendar.utils import generate_slug
from django.contrib.auth.models import User
from mysite.settings import CORS_ALLOWED_ORIGINS
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.urls import reverse

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        # print(request.__dict__)
        new_user = request.user
        user_calendar, created = Calendar.objects.get_or_create(
            user = User.objects.get(username=new_user.username),
            defaults={
                "name": new_user.username,
                "slug": generate_slug(new_user.username)})
        token, created = Token.objects.get_or_create(user=new_user)
        return CORS_ALLOWED_ORIGINS[0] + f"?token={token.key}&slug={user_calendar.slug}"

    def get_signup_redirect_url(self, request):
        new_user = request.user
        user_calendar, created = Calendar.objects.get_or_create(
            user = User.objects.get(username=new_user.username),
            defaults={
                "name": new_user.username,
                "slug": generate_slug(new_user.username)})
        token, created = Token.objects.get_or_create(user=new_user)
        return CORS_ALLOWED_ORIGINS[0] + f"?token={token.key}&slug={user_calendar.slug}"

