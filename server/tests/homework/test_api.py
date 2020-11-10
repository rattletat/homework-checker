import pytest
from django.shortcuts import reverse
from rest_framework import status
from .factories import SubmissionFactory
from tests.accounts.factories import UserFactory


class TestSubmissionAPI:
    @pytest.mark.django_db
    def test_user_can_list_submissions(self, client):
        user = UserFactory(password="testpass123")
        response = client.post(
            reverse("api:login"),
            data={
                "email": user.email,
                "password": "testpass123",
            },
        )
        submissions = [SubmissionFactory(user=user) for _ in range(6)]
        response = client.get(
            reverse("api:submission-list"),
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}",
        )
        assert status.HTTP_200_OK == response.status_code
        assert len(submissions) == len(response.data)
