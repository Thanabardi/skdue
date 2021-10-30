import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar, CalendarEvent, CalendarTag
from .utils import convert_response


class CalendarDetailTests(TestCase):
    pass