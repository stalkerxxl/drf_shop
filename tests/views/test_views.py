import pytest
from django.urls import reverse

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
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Test Category"

    def test_category_create_view(self, api_client):
        url = reverse("category-list")
        data = {"name": "New Category"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert Category.objects.filter(name="New Category").exists()

    def test_category_detail_view(self, api_client, test_category):
        url = reverse("category-detail", args=[test_category.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["name"] == "Test Category"

    def test_category_update_view(self, api_client, test_category):
        url = reverse("category-detail", args=[test_category.id])
        data = {"name": "Updated Category"}
        response = api_client.put(url, data, format="json")
        assert response.status_code == 200
        test_category.refresh_from_db()
        assert test_category.name == "Updated Category"

    def test_category_delete_view(self, api_client, test_category):
        url = reverse("category-detail", args=[test_category.id])
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Category.objects.filter(name="Test Category").exists()
