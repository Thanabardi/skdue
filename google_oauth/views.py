from typing import Mapping
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import os
import requests
import datetime
from google_oauth.models import GoogleAccount
from mysite.settings import BASE_DIR
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from requests.structures import CaseInsensitiveDict
import json
from skdue_calendar.utils import generate_slug
from skdue_calendar.models import Calendar


CREDENTIALS_PATH = os.path.join(BASE_DIR, 'google_oauth', 'credentials.json')
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/calendar.readonly'
    ]


def get_user_info(credentials) -> Mapping:
    """Get user info from authorized accont
    
    Args:
        credentials: authenticated account credential

    Returns:
        Mapping: a dict with keys
            - id, name, given_name, family_name, picture, locale
    """
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    print(user_info)
    return user_info


def generate_new_username(username: str) -> str:
    # check that username is available
    try:
        _ = User.objects.get(username=username)
    except User.DoesNotExist:
        return username
    # try to create new username
    i = 0
    while 1:
        i += 1
        try:
            _ = User.objects.get(username=f"{username}{i}")
        except User.DoesNotExist:
            return f"{username}{i}"


class GoogleLogin(APIView):
    
    def get(self, request):
        # setup cred and api service
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=8040)
        # load user info
        user_info = get_user_info(creds)
        # create account and save token
        google_account, created_new_user = GoogleAccount.objects.get_or_create(
            uuid=user_info["id"],
            defaults={
                "username": user_info["given_name"]
            }
        )
        google_account.token = creds.to_json()
        google_account.save()
        # if new account is created
        if created_new_user:
            # create new User instance
            google_account.linked_username = generate_new_username(google_account.username)
            google_account.save()
            user = User.objects.create(
                username=google_account.linked_username,
                first_name=user_info["given_name"],
                last_name=user_info["family_name"],
                email=user_info["email"]
            )
            calendar = Calendar.objects.create(
                user = user,
                slug = generate_slug(user.username),
                name = user.username
            )

        # create backend access token
        token, created = Token.objects.get_or_create(
            user=User.objects.get(username=google_account.linked_username)
        )
        # login to the backend system
        user = User.objects.get(username=google_account.linked_username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        # return response
        return Response({
            "user_info": user_info,
            "created": created_new_user,
            "id": google_account.uuid,
            "token": token.key
        })


class GoogleLoginSuccess(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({"token": token.key})


class GoogleLogout(APIView):
    # comment line below if you want to test only in back-end
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({"msg": "token expired"})


class GoogleSyncEvent(APIView):
    # comment line below if you want to test only in back-end
    # authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, requset):
        if requset.user:
            cred_path = CREDENTIALS_PATH
            # try to get existed token from google account data
            try:
                google_account = GoogleAccount.objects.get(
                    linked_username=requset.user.username
                )
            except GoogleAccount.DoesNotExist:
                return Response({"msg": "This account is not Google Account"}, HTTP_400_BAD_REQUEST)
            # load credentials
            creds = Credentials.from_authorized_user_info(json.loads(google_account.token), SCOPES)
            if not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    # save new token
                    google_account.token = creds.to_json()
                    google_account.save()
                else:
                    flow = InstalledAppFlow(cred_path, SCOPES)
                    creds = flow.run_local_server(port=8040)
            # build service
            calendar_service = build('calendar', 'v3', credentials=creds)
            # load event data
            all_events = []
            events = calendar_service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
            all_events.append(events)

            # DEBUG: pls remove this after you implement the sync data
            for i in all_events:
                for j in i['items']:
                    print(j['summary'])
                    print(j['start'])
                    print(j['end'])
                    

            # TODO: implement sync data function here (using `google` event tag to create new events)

            return Response({"msg": all_events})
        return Response({"msg": "you are not logged in"}, HTTP_401_UNAUTHORIZED)
