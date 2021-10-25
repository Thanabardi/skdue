from django.contrib import admin
from .models import Calendar, CalendarEvent

admin.site.register(Calendar)
admin.site.register(CalendarEvent)
