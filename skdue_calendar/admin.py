from django.contrib import admin

from .models import Calendar, CalendarEvent, CalendarTag, FollowStatus

admin.site.register(Calendar)
admin.site.register(CalendarEvent)
admin.site.register(CalendarTag)
admin.site.register(FollowStatus)
