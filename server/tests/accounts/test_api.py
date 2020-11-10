import base64
import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from .factories import UserFactory

PASSWORD = "pAssw0rd!"


@pytest.mark.django_db
class TestAuthentication:
    def test_user_can_sign_up(self, client):
        response = client.post(
            reverse("api:signup"),
            data={
                "email": "user@example.com",
                "full_name": "Gary Cole",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        user = get_user_model().objects.last()
        assert status.HTTP_201_CREATED == response.status_code
        assert response.data["id"] == user.id
        assert response.data["email"] == user.email

    def test_user_can_log_in(self, client):
        user = UserFactory(password=PASSWORD)
        data = {
            "email": user.email,
            "password": PASSWORD,
        }
        url = reverse("api:login")
        response = client.post(url, data=data)

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        assert status.HTTP_200_OK == response.status_code
        assert response.data["refresh"]
        assert payload_data["id"] == user.id
        assert payload_data["email"] == user.email
