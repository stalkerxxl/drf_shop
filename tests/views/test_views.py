import pytest
from django.urls import reverse
from rest_framework import status

from shop_api.models import Category
from tests.views.conftest import api_client


@pytest.mark.django_db
class TestCategoryViewSet:
    @pytest.fixture
    def test_category(self):
        return Category.objects.create(name="Test Category")

    def test_category_list_view(self, api_client, test_category):
        url = reverse("category-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Test Category"

    def test_category_detail_view(self, api_client, test_category):
        url = reverse("category-detail", args=[test_category.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Test Category"

    def test_category_create_view_as_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("category-list")
        data = {"name": "New Category"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="New Category").exists()

    def test_category_create_view_as_normal_user(self, api_client, normal_user):
        api_client.force_authenticate(user=normal_user)
        url = reverse("category-list")
        data = {"name": "New Category"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_category_update_view_as_admin(self, api_client, admin_user, test_category):
        api_client.force_authenticate(user=admin_user)
        url = reverse("category-detail", args=[test_category.id])
        data = {"name": "Updated Category"}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        test_category.refresh_from_db()
        assert test_category.name == "Updated Category"

    def test_category_update_view_as_normal_user(
            self, api_client, normal_user, test_category
    ):
        api_client.force_authenticate(user=normal_user)
        url = reverse("category-detail", args=[test_category.id])
        data = {"name": "Updated Category"}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_category_delete_view_as_admin(self, api_client, admin_user, test_category):
        api_client.force_authenticate(user=admin_user)
        url = reverse("category-detail", args=[test_category.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(name="Test Category").exists()

    def test_category_delete_view_as_normal_user(
            self, api_client, normal_user, test_category
    ):
        api_client.force_authenticate(user=normal_user)
        url = reverse("category-detail", args=[test_category.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
