from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.core import exceptions
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def _extract_fields(self, form_data):
        data = {
            key: value
            for key, value in form_data.items()
            if key not in ("password1", "password2")
        }
        data["password"] = form_data["password1"]
        return data

    def validate(self, form_data):
        if form_data["password1"] != form_data["password2"]:
            raise serializers.ValidationError("Passwords must match!")

        data = self._extract_fields(form_data)
        try:
            validators.validate_password(
                password=data["password"], user=get_user_model()(**data)
            )

        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages[0])

        return super(UserSerializer, self).validate(form_data)

    def validate_email(self, value):
        normalized_email = value.lower()
        if get_user_model().objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError(
                "User with this email address already exists."
            )
        return normalized_email

    def create(self, validated_data):
        data = self._extract_fields(validated_data)
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "identifier",
            "password1",
            "password2",
            "name",
        )
        extra_kwargs = {"identifier": {"required": False}}
        read_only_fields = ("id",)


class LogInSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": "Wrong password."}

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
