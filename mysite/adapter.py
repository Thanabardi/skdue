from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from skdue_calendar.models import *
from skdue_calendar.utils import generate_slug
from django.contrib.auth.models import User
from mysite.settings import CORS_ALLOWED_ORIGINS
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.urls import reverse
from mysite.settings import BASE_DIR

from skdue_calendar.views import *


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

    for j in events['items']:
        list =[]
        # print(j['summary'])
        # print(j['start'])
        # print(j['end'])
        # try:
        #     print(j['description'])
        # except KeyError:
        #     print('no description')
        list.append(j['summary'])
        list.append(j['start'])
        list.append(j['end'])
        try:
            list.append(j['description'])
        except KeyError:
            list.append('no description')
        all_events.append(list)
    return all_events

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        events = google_calendar_api()
        print(events)
        #event is big list contain lists of event while in list of event is dict with
        # summary (title) start (start date and time) end (end date and time) description (description)


        new_user = request.user
        user_calendar, created = Calendar.objects.get_or_create(
            user = User.objects.get(username=new_user.username),
            defaults={
                "name": new_user.username,
                "slug": generate_slug(new_user.username)})
        token, created = Token.objects.get_or_create(user=new_user)

        # google_tag_type = CalendarTagType.objects.create(tag_type='google')
        # google_tag = CalendarTag.objects.create(
        #     user=new_user,
        #     tag='google',
        #     tag_type=google_tag_type,
        #     tag_color='blue'
        #     )


        print(events[0][1]['date'])
        print(events[1][1]['dateTime'][:19])
        print(len(events))

        # tag = CalendarTagType(tag_type="google")
        DEFAULT_TAG_TYPE = CalendarTagType.objects.get(tag_type="default")
        DEFAULT_TAG_TYPE.save()
        #delete old tag
        old_tag = CalendarTag.objects.get(user=new_user, tag='google_d', tag_type=DEFAULT_TAG_TYPE)
        old_tag.delete()

        test_tag = CalendarTag.objects.create(user=new_user, tag='google_d', tag_type=DEFAULT_TAG_TYPE)
        test_tag.save()

        user_cal = Calendar.objects.get(name='patkamon')


        for i in range(len(events)):
            try:
                start_time = events[i][1]['date'][:19]
                end_time = events[i][2]['date'][:19]
            except:
                start_time = events[i][1]['dateTime'][:19]
                end_time = events[i][2]['dateTime'][:19]

            if events[i][3] != 'no description':
                desc = events[i][3]
            else:
                desc = ''

            event = CalendarEvent.objects.create(
                    calendar=user_cal,
                    name=events[i][0],
                    slug=generate_slug(events[i][0]),
                    description=desc,
                    start_date = start_time,
                    end_date = end_time,
                    tag = test_tag
            )


        return CORS_ALLOWED_ORIGINS[0] + f"?token={token.key}&slug={user_calendar.slug}"

    def get_signup_redirect_url(self, request):
        new_user = request.user
        user_calendar, created = Calendar.objects.get_or_create(
            user = User.objects.get(username=new_user.username),
            defaults={
                "name": new_user.username,
                "slug": generate_slug(new_user.username)})
        token, created = Token.objects.get_or_create(user=new_user)

        google_tag_type = CalendarTagType.objects.create(tag_type='google')
        google_tag = CalendarTag.objects.create(
            user=new_user,
            tag='google',
            tag_type=google_tag_type,
            tag_color='blue'
            )

        event = CalendarEvent.objects.create(
                calendar=user_calendar,
                name='name',
                slug=generate_slug('name'),
                description='description',
                start_date = datetime.datetime.now(),
                end_date = datetime.date.today() + datetime.timedelta(days=1),
                tag = google_tag
        )


        return CORS_ALLOWED_ORIGINS[0] + f"?token={token.key}&slug={user_calendar.slug}"
