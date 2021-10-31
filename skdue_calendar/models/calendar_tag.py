from django.contrib.auth.models import User
from django.db import models
from .calendar import Calendar
from .calendar_tag_type import CalendarTagType
from skdue_calendar.utils import generate_tag


class CalendarTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    tag = models.CharField(max_length=15)
    # tag_text = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    tag_type = models.ForeignKey(CalendarTagType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tag

    @property
    def tag_type_text(self):
        return str(self.tag_type)

    @classmethod
    def is_valid(self, tag: str, calendar_slug) -> bool:
        tag = generate_tag(tag["tag"])
        can_create = True
        try:
            calendar = Calendar.objects.get(slug=calendar_slug)
            for event in calendar.calendarevent_set.all():
                if event.tag == tag:
                    can_create = False
                    break
        except:
            return True # tag is not found

        return can_create