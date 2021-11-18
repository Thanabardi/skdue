from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from skdue_calendar.models import Calendar
from skdue_calendar.utils import generate_slug
from django.contrib.auth.models import User
from mysite.settings import CORS_ALLOWED_ORIGINS
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.urls import reverse
from mysite.settings import BASE_DIR

import os
import requests
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from requests.structures import CaseInsensitiveDict
import json

import google

Combined_calendar_data = []
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def google_calendar_api():
    cred_path = os.path.join(BASE_DIR, "mysite", "credentials.json")
    all_events=[]
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=8040)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'z'
    # events = service.events().list(calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime').execute()
    events = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
    all_events.append(events)
    for i in all_events:
        for j in i['items']:
            print(j['summary'])
            print(j['start'])
            print(j['end'])
    return all_events

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        events = google_calendar_api()
        print(events)
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

