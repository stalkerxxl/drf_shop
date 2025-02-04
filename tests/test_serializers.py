import pytest

from shop_api.models import Category, Product
from shop_api.serializers import CategorySerializer


@pytest.mark.skip
@pytest.mark.django_db
class TestCategorySerializer:
    def test_category_serializer(self):
        category = Category.objects.create(name="Test Category")
        Product.objects.create(
            name="Product 1", category=category, in_stock=50, price=10.0
        )
        Product.objects.create(
            name="Product 2", category=category, in_stock=10, price=20.0
        )

        # Сериализуем категорию
        serializer = CategorySerializer(category, context={"request": None})
        data = serializer.data

        # Проверяем данные сериалайзера
        assert data["name"] == "Test Category"
        assert data["product_count"] == 2

    # Проверяем, что данные сериалайзера содержат все поля модели
    def test_category_serializer_fields(self):
        category = Category.objects.create(name="Test Category3")
        serializer = CategorySerializer(category, context={"request": None})
        data = serializer.data
        assert set(data.keys()) == set(CategorySerializer.Meta.fields)
