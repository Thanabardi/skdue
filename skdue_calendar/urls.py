from django.urls import path
from .views import *

app_name = "skdue_calendar"
urlpatterns = [
    path('', CalendarList.as_view(), name="list"),
    path('search/', Search.as_view(), name="search"),
    path('<slug:calendar_slug>/', CalendarEventList.as_view(), name="event_list"),
    path('<slug:calendar_slug>/<slug:event_slug>/', CalendarEventDetail.as_view(), name="event_detail"),
]
