from django.db import models


class CalendarTagType(models.Model):
    """Type of calendar tag
    
    type id:
        default: anyone can use this tag
        custom: only creator can use this tag
        private: only use for private event
    """
    tag_type = models.TextField(max_length=32)

    def __str__(self):
        return self.tag_type
