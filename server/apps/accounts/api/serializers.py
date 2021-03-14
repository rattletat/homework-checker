from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        data = {
            key: value
            for key, value in validated_data.items()
            if key not in ("password1", "password2")
        }
        data["password"] = validated_data["password1"]
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "identifier",
            "password1",
            "password2",
            "full_name",
        )
        extra_kwargs = {'identifier': {'required': False}}
        read_only_fields = ("id",)

    def validate_email(self, value):
        normalized_email = value.lower()
        if get_user_model().objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("User with this email address already exists.")
        return normalized_email


class LogInSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token

    def validate_email(self, value):
        return value.lower()
