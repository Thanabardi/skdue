from django.urls import path
from skdue_calendar.api.v2.views import *


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
    path('me', UserMeView.as_view(), name="me"),
    path('me/follow', UserMeFollowedView.as_view(), name="me_follow"),
    path('me/add_new_tag', UserMeAddTagView.as_view(), name="me_add_new_tag"),
    path('me/<calendar_slug>', UserMeCalendarView.as_view(), name="me_calendar"),

    path('get-auth-token', GetAuthToken.as_view(), name="get_auth_token"),
]
