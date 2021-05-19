from rest_framework import serializers
from common.serializers import CitySerializer
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth import authenticate


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        if username is None:
            raise serializers.ValidationError(
                "An username is required to log in."
            )
        if password is None:
            raise serializers.ValidationError(
                "A password is required to log in."
            )

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this username and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This user has been deactivated."
            )
        user = Profile.objects.get(user__username=username).role
        if user != "mentor":
            raise serializers.ValidationError("Ошибка прав доступа")

        return data


class ProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer(required=False, read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "city"]
