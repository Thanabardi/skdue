import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from skdue_calendar.models import Calendar
from .utils import convert_response


class CalendarListTests(TestCase):
    pass