import pytest
from .accounts.factories import UserFactory


@pytest.fixture()
def authclient(client):
    user = UserFactory(password="testpass123")
    client.login(username=user.email, password="testpass123")
    yield client
