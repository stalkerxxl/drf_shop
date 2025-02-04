import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from shop_api.models import Product, Category


class TestOnlyActiveProductsFilter:
    @pytest.fixture
    def product_data(self):
        category = Category.objects.create(name="Test Category")
        Product.objects.create(
            name="Active Product",
            category=category,
            price=100,
            in_stock=10,
            is_active=True,
        )
        Product.objects.create(
            name="Inactive Product",
            category=category,
            price=200,
            in_stock=5,
            is_active=False,
        )

    def test_only_active_products_filter_for_staff_user(
            self, api_client, admin_user, product_data
    ):
        api_client.force_authenticate(user=admin_user)
        url = reverse("products-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_only_active_products_filter_for_normal_user(
            self, api_client, normal_user, product_data
    ):
        api_client.force_authenticate(user=normal_user)
        url = reverse("products-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Active Product"
