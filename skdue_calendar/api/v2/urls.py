from django.urls import path
from skdue_calendar.api.v2.views import *
from skdue_calendar.api.v2.views.calendar_login import Login
from skdue_calendar.api.v2.views.calendar_logout import Logout
from skdue_calendar.api.v2.views.calendar_register import Register

app_name = "api_v2"
urlpatterns = [
    path('calendar/', CalendarListView.as_view(), name="calendar_list"),
    path('calendar/<calendar_slug>', CalendarDetailView.as_view(), name="calendar_detail"),
    path('calendar/<calendar_slug>/<event_slug>', EventDetailView.as_view(), name="event_detail"),
    path('search', SearchView.as_view(), name="search"),
    path('users', UserListView.as_view(), name="user_list"),
    path('login', Login.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),
    path('register', Register.as_view(), name="register"),
    path('fs/', FollowStatusView.as_view(), name="follow_status"),
]
