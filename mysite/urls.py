from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from mysite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/calendar/', include('skdue_calendar.urls')),
    path('api/v2/', include('skdue_calendar.api.v2.urls')),
    path('oauth/', include('google_oauth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
