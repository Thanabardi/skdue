from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.http import response
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.utils.translation import deactivate_all
from skdue_calendar.models import *
from skdue_calendar.utils import generate_slug
from .utils import convert_response
import json


class SearchTests(TestCase):
    pass