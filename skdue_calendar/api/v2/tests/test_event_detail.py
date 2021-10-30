import json
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from skdue_calendar.models import Calendar, CalendarEvent, CalendarTag
from .utils import convert_response


class EventDetailTests(TestCase):
    pass