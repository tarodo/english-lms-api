from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'name')

    def create(self, validated_data):
        """Creates a new user"""
        return get_user_model().objects.create_user(**validated_data)
