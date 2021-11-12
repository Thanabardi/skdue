from django.contrib import admin

from skdue_calendar.models.calendar_tag_type import CalendarTagType

from .models import *

admin.site.register(Calendar)
admin.site.register(CalendarEvent)
admin.site.register(CalendarTag)
admin.site.register(CalendarTagType)
admin.site.register(FollowStatus)
admin.site.register(UserSetting)
