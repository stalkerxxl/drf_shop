import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        username="admin", password="admin123", email="admin@example.com"
    )


@pytest.fixture
def normal_user(django_user_model):
    return django_user_model.objects.create_user(
        username="user", password="user123", email="user@example.com"
    )
