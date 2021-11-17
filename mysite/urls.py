from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from mysite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/calendar/', include('skdue_calendar.urls')),
    path('api/v2/', include('skdue_calendar.api.v2.urls')),
    path('accounts/', include('allauth.urls')), # new
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

