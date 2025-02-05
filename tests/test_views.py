import pytest
from django.urls import reverse
from rest_framework import status

from shop_api.models import Category, Product, Tag, Comment
from shop_api.paginators import ProductsPagination


@pytest.mark.django_db
class TestTagViewSet:
    @pytest.fixture
    def tag_data(self):
        return {"name": "New Tag"}

    @pytest.fixture
    def tag_with_products(self):
        tag = Tag.objects.create(name="Test Tag")
        for i in range(15):
            product = Product.objects.create(
                name=f"Product {i + 1}",
                category=Category.objects.create(name=f"Category {i + 1}"),
                description="Test Description",
                price=100,
                in_stock=10,
                is_active=True,
            )
            product.tags.add(tag)
        return tag

    def test_tag_list(self, api_client, tag_with_products):
        url = reverse("tags-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) > 0
        assert "next" in response.data
        assert "previous" in response.data

    def test_tag_create_admin(self, api_client, admin_user, tag_data):
        api_client.force_authenticate(user=admin_user)
        url = reverse("tags-list")
        response = api_client.post(url, tag_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Tag.objects.filter(name="New Tag").exists()

    def test_tag_create_normal_user(self, api_client, normal_user, tag_data):
        api_client.force_authenticate(user=normal_user)
        url = reverse("tags-list")
        response = api_client.post(url, tag_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_tag_update_admin(self, api_client, admin_user, tag_data):
        api_client.force_authenticate(user=admin_user)
        tag = Tag.objects.create(name="Old Tag")
        url = reverse("tags-detail", args=[tag.id])
        response = api_client.put(url, tag_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Tag.objects.filter(name="New Tag").exists()

    def test_tag_update_normal_user(self, api_client, normal_user, tag_data):
        api_client.force_authenticate(user=normal_user)
        tag = Tag.objects.create(name="Old Tag")
        url = reverse("tags-detail", args=[tag.id])
        response = api_client.put(url, tag_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_tag_delete_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        tag = Tag.objects.create(name="Test Tag")
        url = reverse("tags-detail", args=[tag.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Tag.objects.filter(id=tag.id).exists()

    def test_tag_delete_normal_user(self, api_client, normal_user):
        api_client.force_authenticate(user=normal_user)
        tag = Tag.objects.create(name="Test Tag")
        url = reverse("tags-detail", args=[tag.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Tag.objects.filter(id=tag.id).exists()

    def test_tag_products_list(self, api_client, tag_with_products):
        url = reverse("tags-products", args=[tag_with_products.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == ProductsPagination.page_size
        assert "next" in response.data
        assert "previous" in response.data


@pytest.mark.django_db
class TestCategoryViewSet:
    @pytest.fixture
    def category_data(self):
        return {"name": "New Category"}

    @pytest.fixture
    def category_with_products(self):
        category = Category.objects.create(name="Test Category")
        for i in range(15):
            Product.objects.create(
                name=f"Product {i + 1}",
                category=category,
                description="Test Description",
                price=100,
                in_stock=10,
                is_active=True,
            )
        return category

    def test_category_list(self, api_client, category_with_products):
        url = reverse("categories-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) > 0
        assert "next" in response.data
        assert "previous" in response.data

    def test_category_create_admin(self, api_client, admin_user, category_data):
        api_client.force_authenticate(user=admin_user)
        url = reverse("categories-list")
        response = api_client.post(url, category_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="New Category").exists()

    def test_category_create_normal_user(self, api_client, normal_user, category_data):
        api_client.force_authenticate(user=normal_user)
        url = reverse("categories-list")
        response = api_client.post(url, category_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_category_update_admin(self, api_client, admin_user, category_data):
        api_client.force_authenticate(user=admin_user)
        category = Category.objects.create(name="Old Category")
        url = reverse("categories-detail", args=[category.id])
        response = api_client.put(url, category_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Category.objects.filter(name="New Category").exists()

    def test_category_update_normal_user(self, api_client, normal_user, category_data):
        api_client.force_authenticate(user=normal_user)
        category = Category.objects.create(name="Old Category")
        url = reverse("categories-detail", args=[category.id])
        response = api_client.put(url, category_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_category_delete_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        category = Category.objects.create(name="Test Category")
        url = reverse("categories-detail", args=[category.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=category.id).exists()

    def test_category_delete_normal_user(self, api_client, normal_user):
        api_client.force_authenticate(user=normal_user)
        category = Category.objects.create(name="Test Category")
        url = reverse("categories-detail", args=[category.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Category.objects.filter(id=category.id).exists()

    def test_category_products_list(self, api_client, category_with_products):
        url = reverse("categories-products", args=[category_with_products.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == ProductsPagination.page_size
        assert "next" in response.data
        assert "previous" in response.data


@pytest.mark.django_db
class TestProductViewSet:
    @pytest.fixture
    def product_data(self):
        category = Category.objects.create(name="Test Category")
        return {
            "name": "New Product",
            "category": category.id,
            "description": "Test Description",
            "price": 100,
            "in_stock": 10,
        }

    @pytest.fixture
    def product_with_tags(self):
        category = Category.objects.create(name="Test Category")
        product = Product.objects.create(
            name="Test Product",
            category=category,
            description="Test Description",
            price=100,
            in_stock=10,
            is_active=True,
        )
        for i in range(5):
            tag = Tag.objects.create(name=f"Tag {i + 1}")
            product.tags.add(tag)
        return product

    def test_product_list(self, api_client, product_with_tags):
        url = reverse("products-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) > 0
        assert "next" in response.data
        assert "previous" in response.data

    def test_product_create_admin(self, api_client, admin_user, product_data):
        api_client.force_authenticate(user=admin_user)
        url = reverse("products-list")
        response = api_client.post(url, product_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name="New Product").exists()

    def test_product_create_normal_user(self, api_client, normal_user, product_data):
        api_client.force_authenticate(user=normal_user)
        url = reverse("products-list")
        response = api_client.post(url, product_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_product_update_admin(self, api_client, admin_user, product_data):
        api_client.force_authenticate(user=admin_user)
        product = Product.objects.create(
            name="Old Product",
            category=Category.objects.create(name="Old Category"),
            description="Old Description",
            price=50,
            in_stock=5,
        )
        url = reverse("products-detail", args=[product.id])
        response = api_client.put(url, product_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Product.objects.filter(name="New Product").exists()

    def test_product_update_normal_user(self, api_client, normal_user, product_data):
        api_client.force_authenticate(user=normal_user)
        product = Product.objects.create(
            name="Old Product",
            category=Category.objects.create(name="Old Category"),
            description="Old Description",
            price=50,
            in_stock=5,
        )
        url = reverse("products-detail", args=[product.id])
        response = api_client.put(url, product_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_product_delete_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        product = Product.objects.create(
            name="Test Product",
            category=Category.objects.create(name="Test Category"),
            description="Test Description",
            price=100,
            in_stock=10,
        )
        url = reverse("products-detail", args=[product.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(id=product.id).exists()

    def test_product_delete_normal_user(self, api_client, normal_user):
        api_client.force_authenticate(user=normal_user)
        product = Product.objects.create(
            name="Test Product",
            category=Category.objects.create(name="Test Category"),
            description="Test Description",
            price=100,
            in_stock=10,
        )
        url = reverse("products-detail", args=[product.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Product.objects.filter(id=product.id).exists()


@pytest.mark.django_db
class TestCommentViewSet:
    @pytest.fixture
    def comment_data(self):
        category = Category.objects.create(name="Test Category")
        product = Product.objects.create(
            name="Test Product",
            category=category,
            description="Test Description",
            price=100,
            in_stock=10,
        )
        return {
            "product": product.id,
            "text": "Test Comment",
        }

    @pytest.fixture
    def comment(self, admin_user):
        category = Category.objects.create(name="Test Category")
        product = Product.objects.create(
            name="Test Product",
            category=category,
            description="Test Description",
            price=100,
            in_stock=10,
        )
        return Comment.objects.create(
            user=admin_user,
            product=product,
            text="Test Comment",
        )

    def test_comment_list(self, api_client, comment):
        url = reverse("comments-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) > 0
        assert "next" in response.data
        assert "previous" in response.data

    def test_comment_create(self, api_client, admin_user, comment_data):
        api_client.force_authenticate(user=admin_user)
        url = reverse("comments-list")
        response = api_client.post(url, comment_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.filter(text="Test Comment").exists()

    def test_comment_update_author(self, api_client, admin_user, comment):
        api_client.force_authenticate(user=admin_user)
        url = reverse("comments-detail", args=[comment.id])
        response = api_client.patch(url, {"text": "Updated Comment"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Comment.objects.filter(text="Updated Comment").exists()

    def test_comment_update_non_author(self, api_client, normal_user, comment):
        api_client.force_authenticate(user=normal_user)
        url = reverse("comments-detail", args=[comment.id])
        response = api_client.patch(url, {"text": "Updated Comment"}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_comment_delete_author(self, api_client, admin_user, comment):
        api_client.force_authenticate(user=admin_user)
        url = reverse("comments-detail", args=[comment.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=comment.id).exists()

    def test_comment_delete_non_author(self, api_client, normal_user, comment):
        api_client.force_authenticate(user=normal_user)
        url = reverse("comments-detail", args=[comment.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Comment.objects.filter(id=comment.id).exists()
