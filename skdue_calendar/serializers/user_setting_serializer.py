from rest_framework import serializers
from skdue_calendar.models import UserSetting


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = (
            'user',
            'display_name', 
            'image',
            'about',
            'theme_type',
            'theme_name'
        )
