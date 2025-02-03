import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop_api.models import Category, Product, User
from shop_api.paginators import ProductsPagination


@pytest.mark.django_db
class TestCategoryListCreateAPIView:
    @pytest.fixture
    def category_data(self):
        return {"name": "New Category"}

    @pytest.fixture
    def client(self):
        return APIClient()

    def test_category_list(self, client, admin_user):
        client.force_authenticate(user=admin_user)
        url = reverse("categories-list-create")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_category_create(self, client, admin_user, category_data):
        client.force_authenticate(user=admin_user)
        url = reverse("categories-list-create")
        response = client.post(url, category_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="New Category").exists()

    def test_unauthorized_access(self, client, category_data):
        url = reverse("categories-list-create")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = client.post(url, category_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCategoryRetrieveUpdateDestroyAPIView:
    @pytest.fixture
    def admin_user(self):
        return User.objects.create_superuser(username="admin", password="admin123")

    @pytest.fixture
    def category(self):
        category = Category.objects.create(name="Test Category")
        for i in range(10):
            Product.objects.create(
                name=f"Product {i + 1}",
                category=category,
                description="Test Description",
                price=100,
                in_stock=10,
            )
        return category

    @pytest.fixture
    def client(self):
        return APIClient()

    def test_category_retrieve(self, client, admin_user, category):
        client.force_authenticate(user=admin_user)
        url = reverse("category-retrieve-update-destroy", args=[category.id])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["category"]["name"] == "Test Category"
        assert len(response.data["products"]["results"]) == ProductsPagination.page_size

    def test_category_update(self, client, admin_user, category):
        client.force_authenticate(user=admin_user)
        url = reverse("category-retrieve-update-destroy", args=[category.id])
        update_data = {"name": "Updated Category"}
        response = client.put(url, update_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Category"

    def test_category_delete(self, client, admin_user, category):
        client.force_authenticate(user=admin_user)
        url = reverse("category-retrieve-update-destroy", args=[category.id])
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=category.id).exists()

    def test_unauthorized_access(self, client, category):
        url = reverse("category-retrieve-update-destroy", args=[category.id])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        update_data = {"name": "Updated Category"}
        response = client.put(url, update_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pagination(self, client, admin_user, category):
        client.force_authenticate(user=admin_user)
        url = reverse("category-retrieve-update-destroy", args=[category.id])
        response = client.get(url, {"page": 2})
        assert response.status_code == status.HTTP_200_OK
        assert "next" in response.data["products"]
        assert "previous" in response.data["products"]
        assert len(response.data["products"]["results"]) <= 5
