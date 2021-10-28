from django.urls import path
from skdue_calendar.api.v2.views import *

app_name = "api_v2"
urlpatterns = [
    path('calendar/', CalendarList.as_view(), name="calendar_list"),
    path('calendar/<calendar_slug>', CalendarDetail.as_view(), name="calendar_detail"),
    path('calendar/<calendar_slug>/<event_slug>', EventDetail.as_view(), name="event_detail"),
    path('search', Search.as_view(), name="search"),
    path('users', UserList.as_view(), name="user_list"),
]