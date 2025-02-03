from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from shop_api.models import Category, Product, Tag


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "product_count",
        )


class TagSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "product_count",
        )


class ProductSerializer(serializers.ModelSerializer):
    category = PrimaryKeyRelatedField(many=False, queryset=Category.objects.all())
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "in_stock",
            # "image",
            "is_active",
            "category",
            "tags",
        )
