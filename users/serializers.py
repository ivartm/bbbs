from rest_framework import serializers

# from common.models import City
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = ['id', 'user', 'city']
        fields = ['id', 'user']
