from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import Profile


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        if username is None:
            raise serializers.ValidationError("Введите имя пользователя.")
        if password is None:
            raise serializers.ValidationError("Введите пароль.")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                "Пользователь с таким логином или паролем не найден."
            )

        if not user.is_active:
            raise serializers.ValidationError("Пользователь заблокирован.")
        if not user.profile.is_mentor:
            raise serializers.ValidationError("Ошибка прав доступа.")

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "city"]
