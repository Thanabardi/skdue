from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/calendar/', include('skdue_calendar.urls')),
    path('api/v2/', include('skdue_calendar.api.v2.urls')),
]
