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

# tag constant
try:
    DEFAULT_TAG_TYPE = CalendarTagType.objects.get(tag_type="default")
except CalendarTagType.DoesNotExist:
    tag = CalendarTagType(tag_type="default")
    tag.save()
    DEFAULT_TAG_TYPE = CalendarTagType.objects.get(tag_type="default")

try:
    PRIVATE_TAG_TYPE = CalendarTagType.objects.get(tag_type="private")
except CalendarTagType.DoesNotExist:
    tag = CalendarTagType(tag_type="private")
    tag.save()
    PRIVATE_TAG_TYPE = CalendarTagType.objects.get(tag_type="private")

try:
    CUSTOM_TAG_TYPE = CalendarTagType.objects.get(tag_type="custom")
except CalendarTagType.DoesNotExist:
    tag = CalendarTagType(tag_type="custom")
    tag.save()
    CUSTOM_TAG_TYPE = CalendarTagType.objects.get(tag_type="custom")