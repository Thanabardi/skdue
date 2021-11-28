from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from skdue_calendar.utils import generate_slug
from .calendar import Calendar
from .calendar_tag import CalendarTag


class CalendarEvent(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tag = models.ForeignKey(CalendarTag, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-start_date',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.calendar.slug}/{self.slug}'

    @property
    def tag_text(self):
        return str(self.tag)

    @classmethod
    def is_valid(self, event_data: str, calendar_slug) -> bool:
        """Validate calendar event from calendar event data
        
        Args:
            event_data: dict for calendar event data
            calendar_slug: slug of calendar

        Returns:
            bool: False, if calendar_slug does not exist or start_date < end_date, True otherwise.
        """
        # we need same calendar name
        slug = generate_slug(event_data["name"])
        try:
            calendar = Calendar.objects.get(slug=calendar_slug)
        except:
            return False # calendar not found

        start_date = datetime.strptime(event_data["start_date"], "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(event_data["end_date"], "%Y-%m-%d %H:%M:%S")
        return start_date < end_date

    @classmethod
    def is_usable_tag(self, tag_name, user_id):
        # try to get default tag
        try:
            queryset = CalendarTag.objects.filter(tag_type__tag_type="default") | CalendarTag.objects.filter(tag_type__tag_type="private")
            _ = queryset.get(tag=tag_name)
            return True
        except CalendarTag.DoesNotExist:
            try:
                user = User.objects.get(id=user_id)
                _ = CalendarTag.objects.filter(user=user).filter(tag_type__tag_type="custom").get(tag=tag_name)
                return True
            except CalendarTag.DoesNotExist:
                return False
        return False
