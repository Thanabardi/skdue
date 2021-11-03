from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Can be use for all things related to User model"""
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email"
        )