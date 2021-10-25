from django.db import models
from skdue_calendar.utils import generate_slug


class Calendar(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'

    @classmethod
    def is_valid(self, calendar_data: dict) -> bool:
        """Validate calendar data for create new calendar.
        
        Args:
            calendar_data: dict for calendar creation

        Returns:
            bool: True, if calendar name does not exist, False otherwise.
        """
        slug = generate_slug(calendar_data["name"])
        try:
            _ = Calendar.objects.get(slug=slug)
        except:
            return True
        return False