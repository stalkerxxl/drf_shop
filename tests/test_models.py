import pytest
from django.core.exceptions import ValidationError

from shop_api.models import Category, Tag


@pytest.mark.django_db
class TestCategoryModel:
    @pytest.fixture
    def test_category(self):
        return Category.objects.create(name="Test Category")

    def test_category_creation(self, test_category):
        _ = Category.objects.filter(name="Test Category").exists()
        assert _ == True, "Category not created"
        assert test_category.name == "Test Category"

    def test_duplicate_category_creation(self, test_category):
        with pytest.raises(ValidationError):
            category = Category(name="Test Category")
            category.full_clean()

    def test_empty_name_category_creation(self):
        with pytest.raises(ValidationError):
            category = Category(name="")
            category.full_clean()

    def test_category_name_max_length(self):
        long_name = "a" * 101
        with pytest.raises(ValidationError):
            category = Category(name=long_name)
            category.full_clean()

    def test_category_str_method(self, test_category):
        assert str(test_category) == "Test Category"


@pytest.mark.django_db
class TestTagModel:
    @pytest.fixture
    def test_tag(self):
        return Tag.objects.create(name="Test Tag")

    def test_tag_creation(self, test_tag):
        _ = Tag.objects.filter(name="Test Tag").exists()
        assert _ == True, "Tag not created"
        assert test_tag.name == "Test Tag"

    def test_duplicate_tag_creation(self, test_tag):
        with pytest.raises(ValidationError):
            tag = Tag(name="Test Tag")
            tag.full_clean()

    def test_empty_name_tag_creation(self):
        with pytest.raises(ValidationError):
            tag = Tag(name="")
            tag.full_clean()

    def test_tag_name_max_length(self):
        long_name = "a" * 51
        with pytest.raises(ValidationError):
            tag = Tag(name=long_name)
            tag.full_clean()

    def test_tag_str_method(self, test_tag):
        assert str(test_tag) == "Test Tag"
