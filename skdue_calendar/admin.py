from django.contrib import admin

from .models import Calendar, CalendarEvent, CalendarTag

admin.site.register(Calendar)
admin.site.register(CalendarEvent)
admin.site.register(CalendarTag)